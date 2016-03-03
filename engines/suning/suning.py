# -*- coding: utf-8 -*-
import urllib2
import os
import time
import sys
import socket
import re
import cookielib

third_url=[] 
starturl='http://list.suning.com/1-262531-0-0-0-9017.html' #提取初始页面，手动换第二级url即可
response_1=urllib2.urlopen(starturl)
html=response_1.readlines()
for line1 in html:
    a=line1.strip()
    pattern_third_url=re.compile(r'.*?<a value=".*?" name=".*?" href=".*?" title=".*?">.*?</a>')
    match_third_url=pattern_third_url.match(a)
    if match_third_url: #找出第三级url
        data_third_url=match_third_url.group()
        data_third_url=''.join(data_third_url)
        third_url_1=data_third_url.split('href="')
        third_url_2=third_url_1[1].split('" title="')
        third_url_3=third_url_2[0].split('-')
        third_url.append(third_url_3[1]) #把第三级url存入third_url
for num in third_url: #找出第三级url对应的每一类有多少页，返回m
 url='http://list.suning.com/1-'+num+'-0-0-0-9017.html'
 page=urllib2.urlopen(url)
 pagetatol=page.readlines()
 for a in pagetatol:
     ab=a.strip()
     pattern1=re.compile(r'param.pageNumbers = ".*?";')
     match1=pattern1.match(ab)
     if match1: 
         data1=match1.group()
         page1=data1.split('= "')
         page2=page1[1].split('";')
         m=int(page2[0])-1
         label=[]
         for i in range(0,m): #打开每一小类的每一页
           try:  
              url1='http://list.suning.com/1-'+num+'-'+str(i)+'-1-0-9017.html'#翻页就是i+1
              b=urllib2.urlopen(url1)
              html1=b.readlines()
              for lines in html1:
               aa=lines.strip()
               pattern2=re.compile(r'<a title=.*?>.*?</a>.*?<a href=.*?>.*?</a><input type=.*?<span>.*?</span></h1>')  
               match2=pattern2.match(aa)
               if match2: #提取标签
                 data2=match2.group()
                 li=data2.split('</a>')#分割字符串找取信息
                 li1=li[1].split('>')
                 label1=li1[-1]
                 li2=li[2].split('>')
                 label2=li2[-1]
                 li3=li[3].split('<span>')
                 li4=li3[1].split('</span>')
                 label3=li4[0]
                 finallabel=label1+','+label2+','+label3 #标签
                 label.append(finallabel) #标签存入label列表
                 n=i+1
                 print 'page '+str(n)+' is ok'                 
               pattern3=re.compile(r'<a title=".*?" target="_blank" href=".*?" name=".*?">')
               match3=pattern3.match(aa)
               if match3: #提取商品信息
                 data3=match3.group()
                 yu=data3.split('href="')#分割字符串找取信息
                 yu1=yu[1].split('" name=')
                 yu2=yu[0].split('title="')
                 yu3=yu2[1].split('" target=')
                 producturl=yu1[0]
                 pid_1=producturl.split('/')
                 pid_2=pid_1[-1].split('.')
                 pid  =pid_2[0]
                 productname=yu3[0]
                 mid=producturl+','+productname+','+label[i]+','+pid  #地址+item+标签+ID 
                 file_obj=open('1.txt','a')
                 file_obj.write(mid+'\n')      
                 file_obj.close()
           except Exception,e: #异常处理，如果断掉可以继续爬取
                  print "error"
                  continue
                 

print 'end'

  
  
  
        
    
    
   



   
