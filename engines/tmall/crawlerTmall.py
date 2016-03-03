#! /usr/bin/env python
# -*- coding=utf-8 -*-
# @Author pythontab.com

import os
import time
import cookielib,urllib2
import socket
import re
import glob
import requests
import json

#os.chdir('E:\\project\\webcrawler\\Tmall\\tmall')
def writeTo(path,data,mode):
    f = file(path,mode)
    f.write(data)
    f.close()
data_dir=''
def crawler(url):
    try:
        '''cj=cookielib.CookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        request = urllib2.Request(url)
        response = opener.open(request).read()'''
        #定制请求头
        payload = {'some': 'data'}
        headers0 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36','Accept':'*/*','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'zh-CN,zh;q=0.8','Cookie':'thw=cn; _tb_token_=0BF9rodqKVV9Ud6; ck1=; v=0; uc1=lltime=1428394414&cookie14=UoW1HJxR%2FMdJeA%3D%3D&existShop=false&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=UIHiLt3xTIkz&tag=7&cookie15=WqG3DMC9VAQiUQ%3D%3D&pas=0; uc3=nk2=3GNqKb%2Fqrw4%3D&id2=UoH8WVRFcoa%2F9w%3D%3D&vt3=F8dAT%2BavuMMIf%2BeOEkE%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; existShop=MTQyODM5NDcxNg%3D%3D; lgc=%5Cu5B54%5Cu5FB7%5Cu94A600; tracknick=%5Cu5B54%5Cu5FB7%5Cu94A600; sg=095; cookie2=1c38f39adfb0b9f0617554ff349bbd6c; mt=np=&ci=0_0; cookie1=BqAJAehj%2F%2BMKUNxYiV9dT5myq5RG6%2FXu%2BH%2ByYVOPS0w%3D; unb=1034437499; t=1362ceddf9d24739f209bbbc0a5d599d; _cc_=U%2BGCWk%2F7og%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu5B54%5Cu5FB7%5Cu94A600; cookie17=UoH8WVRFcoa%2F9w%3D%3D'}
        #headers1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36','Accept':'*/*','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'zh-CN,zh;q=0.8','Cookie':'thw=cn; _tb_token_=0BF9rodqKVV9Ud6; ck1=; v=0; uc1=lltime=1428391346&cookie14=UoW1HJxR%2B0xmSw%3D%3D&existShop=false&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=UtASsssmeW6lpyd%2BB%2B3t&tag=0&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=nk2=2ApX8WlSto14fyg%3D&id2=UUpoa09v4FjJgA%3D%3D&vt3=F8dAT%2BavuMAjJ0pejGc%3D&lg2=URm48syIIVrSKA%3D%3D; existShop=MTQyODM5Mzk3Ng%3D%3D; lgc=%5Cu7070%5Cu8272%5Cu5934%5Cu50CF_92; tracknick=%5Cu7070%5Cu8272%5Cu5934%5Cu50CF_92; sg=240; cookie2=1c38f39adfb0b9f0617554ff349bbd6c; mt=np=&ci=0_0; cookie1=UtAGxwicebgBn%2F8NUzw5%2BisH23LpBQQBubcCSLJ6TNA%3D; unb=2297603454; t=1362ceddf9d24739f209bbbc0a5d599d; _cc_=U%2BGCWk%2F7og%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu7070%5Cu8272%5Cu5934%5Cu50CF_92; cookie17=UUpoa09v4FjJgA%3D%3D'}
        #headers2 = {'content-type': 'application/json',
                   #'Cookie':'cna=uDSqDYtmGAcCAXL/KALKyWHa; isg=0B378BE265E769A9C47E5D826B4E7254; _tb_token_=hQl8ZO1YzSkZ45A; ck1=; uc1=lltime=1428372740&cookie14=UoW1HJxfTnOp5Q%3D%3D&existShop=false&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=VFC%2FuZ9aiKIc&tag=2&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0; uc3=nk2=3v5OY7G8u%2B8%3D&id2=Vyh61UuMNReJ&vt3=F8dAT%2BavtoMmIih1keg%3D&lg2=UtASsssmOIJ0bQ%3D%3D; lgc=%5Cu5EFA%5Cu5149%5Cu519B66; tracknick=%5Cu5EFA%5Cu5149%5Cu519B66; cookie2=1c8f52ef38ff4d610a2b79a02ea4b881; cookie1=VAMUTWp9UyvfBgwbK0EC5z3dEGZ7WoiQU%2F5bl7%2FZULE%3D; unb=446471490; t=1f2669b32c2031611ab432b26b12c598; _nk_=%5Cu5EFA%5Cu5149%5Cu519B66; _l_g_=Ug%3D%3D; cookie17=Vyh61UuMNReJ; login=true; mbk=94aec3b616692025'}       
        #headerslist=[headers0,headers1]
        r = requests.post(url, data=json.dumps(payload), headers=headers0)
        data=r.content
        #response = requests.get(url)  
        #data=response.content
        #print data
        writeTo(data_dir+'category'+ '.html', data, 'w+')      #w+消除文件内容，然后以读写方式打开文件
    except Exception, e:
        print e
        print 'error occured in '+url
def analyze(li,fi):
    for li in fi:
        a=li.strip()
        #标签   必须手动改一级标签
        pattern4=re.compile(r'title=".*?" data-i="cat" data-t="3">.*?</a><i></i>')
        #pattern4=re.compile(r'<a href=".*?" data-i="brand" data-t="4">.*?</a>')
        match4=pattern4.match(a)
        if match4:
            data5=match4.group()
            x3=data5.find('>')
            y4=data5.find('<',x3)
            label2=data5[x3+len('>'):y4]
            
            firstlabel='精品男装'
            label=firstlabel.decode('utf-8').encode('gbk')+','+label2
        '''pattern7=re.compile(r'<input type="text" name="q" value=".*?" class="crumbSearch-input" id="J_CrumbSearchInuput" />')
        match7=pattern7.match(a)
        if match7:
            data8=match7.group()
            x8=data8.find('value')
            y10=data8.find('"',x8)
            y11=data8.find('"',y10+len('"'))
            label2=data8[y10+len('"'):y11]
            label=label2'''
            #firstlabel='女士内衣/男士内衣/家居服'
            #label=firstlabel.decode('utf-8').encode('gbk')+','+label2
            #print lable
        #价格
        pattern6=re.compile(r'<em title=".*?"><b>&yen;</b>.*?</em>')
        match6=pattern6.match(a)
        if match6:
            data7=match6.group()
            x7=data7.find('</b>')
            y9=data7.find('</em>',x7+len('</b>'))
            price=data7[x7+len('</b>'):y9]
            #print price
        #商品
        pattern5=re.compile(r'<a href=".*?" target="_blank" title=".*?" data-p=".*?" >')
        match5=pattern5.match(a)
        if match5:
            data6=match5.group()
            x4=data6.find('"')
            y5=data6.find('"',x4+len('"'))
            itemurl=data6[x4+len('"'):y5]
            shangpinurl='http:'+itemurl
            x5=data6.find('title')
            y6=data6.find('"',x5)
            y7=data6.find('"',y6+len('"'))
            shangpinname=data6[y6+len('"'):y7]
            x6=data6.find('id')
            y8=data6.find('&amp',x6)
            productid=data6[x6+len('id='):y8]
            commodity=productid+','+shangpinurl+','+shangpinname
            file_obj=open('d3.txt','a+')#将匹配出来的东西写入文档
            file_obj.write(commodity+','+price+','+label+'\n')
            file_obj.close()    
'''start_url="http://nvzhuang.tmall.com/?spm=3.7396704.20000007.1.RghZRk&acm=tt-1141518-36998.1003.8.76021&uuid=76021&scm=1003.8.tt-1141518-36998.OTHER_1401830964893_76021&pos=1"
req_header={'User-Agent':'Mozilla/5.0(Windows NT 6.1) AppleWebKit/537.11 (KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accetp-Encoding':'gzip',
'Connection':'close',
'Referer':None
}
req_timeout = 5
req = urllib2.Request(start_url,None,req_header)
resp = urllib2.urlopen(req,None,req_timeout)
data = resp.read()#伪装成一个浏览器
if not os.path.isdir(data_dir):
    os.mkdir(data_dir)
    writeTo(data_dir +'nvzhuang'+ '.html', data, 'w+')
'''
'''b=open('nvzhuang.html','r+').readlines()#以读的方式打开这个文件 
for line in b:
    a=line.strip()
    pattern1=re.compile(r'<a class=".*?" href=".*?"  target="_blank">')
    match1=pattern1.match(a)
    if match1:
        data1=match1.group()
        m1=data1.find('href')
        n1=data1.find('"',m1)
        n2=data1.find('"',n1+len('"'))
        data2=data1[n1+len('"'):n2]
        #category_url.append(data2)
        file_obj=open('categoryurl.txt','a+')
        file_obj.write(data2+'\n')#将匹配出来的东西写入文档
        file_obj.close()
#print category_url'''

if __name__ == '__main__':
    #flag=0
    i=open('categoryurl.txt','r').readlines()
    for category_url in i:
        category_url1=category_url.rstrip('\n')
        print category_url1
        c1=category_url1.find('&sort')   #把第一页的URL进行分组处理方便剩下的URL重组
        url1=category_url1[:c1]
        url2=category_url1[c1:]
        j=1
        crawler(category_url1)
        f=open('category.html','r+').readlines()#以读的方式打开这个文件
        line1=[]
        analyze(line1,f)
        for line in f:
            a=line.strip()
            #查找一共多少页
            pattern7=re.compile(r'<b class="ui-page-s-len">.*?</b>')
            match7=pattern7.match(a)
            if match7:
                data8=match7.group()
                x8=data8.find('/')
                y10=data8.find('</b>',x8)
                pagesum=data8[x8+len('/'):y10]
                print 'pagesum='+pagesum
                while j<int(pagesum):
                #while j<100:
                    #nextpageurl=url1+'&s='+str(59+60*(j-1))+url2
                    nextpageurl=url1+'&s='+str(60*j)+url2     #重组得到下一页的URL
                    print 'j='+str(j)
                    #flag1=j/5
                    #flag=flag1%2
                    j=j+1
                    crawler(nextpageurl)         #爬取下一页内容
                    f1=open('category.html','r+').readlines()
                    line2=[]
                    analyze(line2,f1)              #解析下一页的内容
                    #time.sleep(3)
                    #break
                    
                print 'end'
                break
        print 'this category end'
    print 'over'
