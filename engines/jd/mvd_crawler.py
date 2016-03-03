#-*- encoding: UTF-8 -*-
import scrapy
import re
import time
class JDmvdSpider(scrapy.Spider):
    name = 'mvdspider'
    start_urls = ['http://mvd.jd.com/']
    pattern1 = re.compile(r'http://channel\.jd\.com/(\d+-\d+)\.html')
    pattern2 = re.compile(r'http://list\.jd\.com/(\d+-\d+-\d+).html')
    pattern3 = re.compile(r'<title>(.*) 【行情 价格 评价 正品行货】-京东</title>')
    pattern4 = re.compile(r'<em>共<b>(\d+)</b>.*?</em>')
    pattern5 = re.compile(r'item\.jd\.com/(\d+)\.html#comments-list')
    id_set = set()
    cat_set = set()
    channel_set = set()
    next_step = []
    def parse(self, response):
        for url in self.pattern1.findall(response.body) :
            channel = url.replace('-',',')
            if channel not in self.channel_set:
                self.channel_set.add(channel)
                next_url = 'http://list.jd.com/list.html?cat='+channel
                self.next_step.append(next_url)
        for url in self.pattern2.findall(response.body):
            cat = url.replace('-',',')
            if cat not in self.cat_set:
                self.cat_set.add(cat)
                next_url = 'http://list.jd.com/list.html?cat='+cat
                self.next_step.append(next_url)
        for each in self.next_step:
            yield scrapy.Request(each,self.parse_subclass)


    def parse_subclass(self, response):
        lab = self.pattern3.findall(response.body)
        label = lab[0].strip()
        label = label.split(' ')
        if len(label)== 3:
            label1 = label[0]
            label2 = label[1]
            label3 = label[2]
        else:
            label1 = ''
            label2 = label[0]
            label3 = '音像'
        pagesum = self.pattern4.findall(response.body)
        if pagesum:
            pagenumber = int(pagesum[0])+1
        else:
            pagenumber = 2
        for pagenum in range(1, pagenumber):
            page_url = response.url+'&page='+str(pagenum)+'&JL=6_0_0'
            time.sleep(0.1)
            yield scrapy.Request(page_url, self.parse_items, meta={'label1': label1,'label2':label2,'label3':label3})

    def parse_items(self, response):
        for product_id in self.pattern5.findall(response.body):
            if product_id not in self.id_set:
                self.id_set.add(product_id)
                yield {'id': product_id, 'label1': response.meta['label1'], 'label2': response.meta['label2'], 'label3': response.meta['label3']}
