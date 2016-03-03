#-*- encoding: UTF-8 -*-
import scrapy
import re
import time
class JDpetSpider(scrapy.Spider):
    name = 'petspider'
    start_urls = ['http://channel.jd.com/pet.html']
    pattern1 = re.compile(r'http://list\.jd\.com/list\.html\?cat=\d+\,\d+\,\d+')
    pattern2 = re.compile(r'<em>共<b>(\d+)</b>.*?</em>')
    pattern3 = re.compile(r'<title>(.*) 【行情 价格 评价 正品行货】-京东</title>')
    pattern4 = re.compile(r'item\.jd\.com/(\d+)\.html#comments-list"')
    petid_set = set()
    catid_set = set()
    def parse(self, response):
        for url in self.pattern1.findall(response.body) :
            catid = url.split('cat=')[1]
            if catid not in self.catid_set:
                self.catid_set.add(catid)
                yield scrapy.Request(url, self.parse_subclass,meta={'cat': catid})

    def parse_subclass(self, response):
        lab = self.pattern3.findall(response.body)
        label = lab[0].strip()
        label1,label2,label3 = label.split(' ')
        pagesum = self.pattern2.findall(response.body)
        if pagesum:
            pagenumber = int(pagesum[0])+1
        else:
            pagenumber = 2
        for pagenum in range(1, pagenumber+1):
            page_url = response.url.replace(',','%2C')+'&page='+str(pagenum)+'&JL=6_0_0'
            time.sleep(0.1)
            yield scrapy.Request(page_url, self.parse_items, meta={'label1': label1,'label2':label2,'label3':label3,'cat':response.meta['cat']})

    def parse_items(self, response):
        for product_id in self.pattern4.findall(response.body):
            if product_id not in self.petid_set:
                self.petid_set.add(product_id)
                yield {'id': product_id, 'label1': response.meta['label1'], 'label2': response.meta['label2'], 'label3': response.meta['label3'],'cat':response.meta['cat']}

