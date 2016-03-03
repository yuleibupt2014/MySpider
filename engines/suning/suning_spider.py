#-*- encoding: UTF-8 -*-
import scrapy
import re
import time

class suningSpider(scrapy.Spider):
    name = 'suningspider'
    start_urls = ['http://www.suning.com/emall/pgv_10052_10051_1_.html']
    pattern1 = re.compile(r'http://list\.suning\.com/.*?\.html')
    pattern2 = re.compile(r'<input type="hidden" value="(.*?)" id="ga_itemDataBean_category_description_name"')
    pattern3 = re.compile(r'class="pageTotal">(\d+)</i>')
    pattern4 = re.compile(r'http://product\.suning\.com/(\d+)\.html#pro_detail_tab')
    id_set = []
    def parse(self, response):
        for url in self.pattern1.findall(response.body) :
            yield scrapy.Request(url, self.parse_subclass)

    def parse_subclass(self, response):
        lab = self.pattern2.findall(response.body)
        if lab:
            label = lab[0].split('" id=')
            label1 = label[0]
            label2 = label[1].split('value="')[-1]
            label3 = label[2].split('value="')[-1]

            pagesum = self.pattern3.findall(response.body)
            if pagesum:
                pagenumber = int(pagesum[0])
                if pagenumber==100:
                    pagenumber = 200
            else:
                pagenumber = 2

            pageurl = response.url
            for pagenum in xrange(pagenumber):
                if pageurl[32]=='0':
                    page_url = pageurl[:32] + str(pagenum) + pageurl[33:]
                else:
                    page_url = pageurl[:31] + str(pagenum) + pageurl[32:]
                time.sleep(0.1)
                yield scrapy.Request(page_url, self.parse_items, meta={'label1': label1,'label2':label2,'label3':label3})

    def parse_items(self, response):
        for product_id in self.pattern4.findall(response.body):
            if product_id not in self.id_set:
                self.id_set.append(product_id)
                yield {'id': product_id, 'label1': response.meta['label1'], 'label2': response.meta['label2'], 'label3': response.meta['label3']}
