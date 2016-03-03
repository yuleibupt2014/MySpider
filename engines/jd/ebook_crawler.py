#-*- encoding: utf-8 -*-
import scrapy
import re
import time
class JDebookSpider(scrapy.Spider):
    name = 'ebookspider'
    start_urls = ['http://channel.jd.com/ebook_allSort.html']
    pattern1 = re.compile(r'http://e\.jd\.com/products/\d+-\d+-\d+\.html')
    pattern2 = re.compile(r'http://e\.jd\.com/products/(\d+-\d+-\d+)\.html')
    pattern3 = re.compile(r'<meta name="Keywords" content="(.*?) " />')
    pattern4 = re.compile(r'>(\d+)</a><a href="\d+-\d+-\d+-1-\d+\.html" class="next">')
    pattern5 = re.compile(r'btnFluent(\d+)')
    id_set = set()
    cat_set = set()
    def parse(self, response):
        for url in self.pattern1.findall(response.body) :
            catid = url.split('/')[-1]
            catid = catid.split('.html')[0]
            catid = catid.replace('-',',')
            if catid not in self.cat_set:
                self.cat_set.add(catid)
                yield scrapy.Request(url,self.parse_subclass)


    def parse_subclass(self, response):
        lab = self.pattern3.findall(response.body)
        label = lab[0].strip()
        label = label.split(',')
        if len(label)== 3:
            label1 = label[0].decode('gb2312').encode('utf-8')
            label2 = label[1].decode('gb2312').encode('utf-8')
            label3 = label[2].decode('gb2312').encode('utf-8')
        else:
            label1 = ''
            label2 = ''
            label3 = '电子书'
        pagesum = self.pattern4.findall(response.body)
        if pagesum:
            pagenumber = int(pagesum[0])+1
        else:
            pagenumber = 2
        for pagenum in range(1, pagenumber):
            pageurl = response.url.split('.html')[0]
            page_url = pageurl+'-1-'+str(pagenum)+'.html'
            time.sleep(0.1)
            yield scrapy.Request(page_url, self.parse_items, meta={'label1': label1,'label2':label2,'label3':label3})

    def parse_items(self, response):
        for product_id in self.pattern5.findall(response.body):
            if product_id not in self.id_set:
                self.id_set.add(product_id)
                yield {'id': product_id, 'label1': response.meta['label1'], 'label2': response.meta['label2'], 'label3': response.meta['label3']}

