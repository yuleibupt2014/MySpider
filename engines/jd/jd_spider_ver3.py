#-*- encoding: UTF-8 -*-
import scrapy
import re
import time
class JDSpider(scrapy.Spider):
    name = 'jd_spider'
    start_urls = ['http://www.jd.com/allSort.aspx']
    pattern1 = re.compile(r'http://list\.jd\.com/\d+-\d+-\d+\.html')
    pattern2 = re.compile(r'http://channel\.jd\.com/\d+-\d+\.html')
    pattern3 = re.compile(r'class="crumbs-link">(.*?)</a>')
    pattern4 = re.compile(r'<span class="curr">(.*?)</span>')
    pattern5 = re.compile(r'<title> (.*?) 【行情 价格 评价 正品行货】-京东</title>')
    pattern8 = re.compile(r'<em>共<b>(\d+)</b>.*?</em>')
    pattern0 = re.compile(r'item\.jd\.com/(\d+)\.html#comments-list')
    product_set = set()
    cat_set = set()
    channel_set = set()
    
    def parse(self, response):
        cat_url = self.pattern1.findall(response.body)
        for eachurl in cat_url:
            cat_temp = eachurl.split('com/')[1]
            cat_temp = cat_temp.split('.html')[0]
            self.cat_set.add(cat_temp)
            # a = cat_temp.rfind(',')
            # channel_temp = cat_temp[:a]
            # if channel_temp not in self.channel_set:
            #     self.channel_set.add(channel_temp)
            cat_url = cat_temp.replace('-',',')
            url = 'http://list.jd.com/list.html?cat='+cat_url
            yield scrapy.Request(url,self.parse_subclass,meta = {'cat':cat_temp})
        # channel_url = self.pattern2.findall(response.body)
        # for each in channel_url:
        #     channelid = each.split('com/')[1]
        #     channelid = channelid.split('.html')[0]
        #     channelid = channelid.replace('-',',')
        #     if '1713' not in channelid and channelid not in self.channel_set:
        #         self.channel_set.add(channelid)
        #         self.channel_not_set.add(channelid)
        #         yield scrapy.Request(each, self.parse_catlist)

    # def parse_catlist(self, response):
    #     # list_url = []
    #     caturl = self.pattern1.findall(response.body)
    #     for oneurl in caturl:
    #         temp = oneurl.split('com/')[1]
    #         temp = temp.split('.html')[0]
    #         temp = temp.replace('-',',')
    #         if  temp not in self.cat_set:
    #             self.cat_set.add(temp)
    #             yield scrapy.Request(oneurl, self.parse_subclass,meta={'cat':temp})

    def parse_subclass(self, response):
        lab = self.pattern3.findall(response.body)
        label1 = lab[0]
        label = self.pattern4.findall(response.body)
        if len(label)==2:
            label2 = label[0]
            label3 = label[1]
        else:
            label = self.pattern5.findall(response.body)
            label = label.strip()
            label = label.split(' ')
            if len(label)==3:
                label1 = label[0]
                label2 = label[1]
                label3 = label[2]
            else:
                label2 = ''
                label3 = ''

        pagesum = self.pattern8.findall(response.body)
        if pagesum:
           pagenumber = int(pagesum[0])+1
        else:
           pagenumber = 2
        pageurl = response.url
        # next = pageurl.split('cat=')[1]
        # nexturl = pageurl.split('&')[0]
        # next = pageurl.split('com/')[1]
        # next = next.split('.html')[0]
        # next = next.replace('-','%2C')
        for pagenum in range(1, pagenumber+1):
            page_url = pageurl + '&page='+str(pagenum)+'&JL=6_0_0'
            time.sleep(0.1)
            yield scrapy.Request(page_url, self.parse_items, meta={'label1': label1,'label2': label2,'label3': label3,'cat':response.meta['cat']})

    def parse_items(self, response):
        for product_id in self.pattern0.findall(response.body):
            if product_id not in self.product_set:
                self.product_set.add(product_id)
                yield {'id': product_id, 'label1': response.meta['label1'],'label2': response.meta['label2'],'label3': response.meta['label3']}

