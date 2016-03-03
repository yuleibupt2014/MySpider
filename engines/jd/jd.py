# -*- coding: utf-8 -*-
import urllib2
import os
import time
import sys
import socket
import re
import cookielib
import math
b=open('jd0.txt','r').readlines()
for line in b:
    caoyu=[]
    cao=[]
    try: 
     response=urllib2.urlopen(line)
     html=response.readlines()
     for lines in html:
        n=len(lines)
        caoyu.append(n)
        cao.append(lines)
     m=max(caoyu)#找出最长为内容
     j=caoyu.index(m)
     #找出页数
     l=j+1
     page=''
     page = page.join(cao[l])
     control=re.match(r'</div></div><div class="m-aside">',page)
     if (control==None):
      page1=page.split('<em>共<b>')
      page2=page1[1].split('</b>')
      k=page2[0]     
     else:
      k=1
     pagenumber=int(k)+1
     print k
    except Exception,e: #异常处理，如果断掉可以继续爬取
                  print "error"
                  continue 
    #每一页爬取
    for pagenum in range(1,pagenumber):
        line=line.rstrip()
        pageurl=line+'&page='+str(pagenum)
        print pageurl
        yu=[]
        try:
         response1=urllib2.urlopen(pageurl)
         html1=response1.readlines()
         print 'page'+str(pagenum)+' ok'
         for information in html1:
            yu.append(information)
         #找出分类
         label=''
         label=label.join(yu[19])
         labels=re.findall(r'content="京东JD.COM是国内最专业的 ([^"]+)、 报价、促销、新闻、评论、导购、图片 网上购物商城',label)
         label1=''
         label1=label1.join(labels)
         label0=label1.replace('、',',')
         #找出商品信息
         name0=[]  #名字
         url0=[]   #地址
         pid0=[]   #列表
         pages=''
         pages = pages.join(yu[j])
         names=re.findall(r'<em>([^"]+)/em><i name=',pages)
         urls=re.findall(r'href="([^"]+)l" title="',pages)
         name_1=''
         url_1=''
         name_1 =name_1.join(names)
         url_1=url_1.join(urls)
         name_2=name_1.split('<')
         num=len(name_2) 
         number=num-2   #找出有多少个商品
         for x in name_2[0:-2]:
            name_3 = x
            name0.append(name_3)
         url_2=url_1.split('.htm')
         for y in url_2[0:-2]:
            url_3 = y+'.html'
            pid_1=y.split('/')
            pid_2=pid_1[-1]
            pid0.append(pid_2)
            url0.append(url_3)
         #把分类信息和商品信息分汇总  
         for i in range(0,number):
            item=url0[i]+','+name0[i]+','+pid0[i]+','+label0
            file_obj=open('jd.txt','a')
            file_obj.write(item+'\n')      
            file_obj.close()
        except Exception,e: #异常处理，如果断掉可以继续爬取
                  print "error"
                  pagenum=pagenum-1
                  continue
    
    
       
       
    
    
   

        
    
    
