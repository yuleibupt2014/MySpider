# -*- coding: utf-8 -*-

import sys
import os
import os.path
import requests
import re
import socket
import time
import threading
import m
#定制请求头
headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.0',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'X-Request-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Pragma': 'no-cache',
        }

def request_ajax_data(url,data,referer,label1,label2,label3, catid):

    for i in xrange(2):
        try:
            res = requests.post(url, data=data, headers=headers)
            #print res.content
            if res.status_code != 200 or res.content is "":
                continue

            obj_json = res.json()
            #print obj_json
            products = obj_json['products']

            n=len(products)
            print "get %d" % n   
            if n is 0:
                return False

            file_obj1=open("guomeidd.txt" ,'a+') 
            for j in xrange(n):
                sid = products[j]['pId']#在json表里提取需要的信息
                skuid1=products[j]['skuId']
                print skuid1
                sname = products[j]['skus']['name']
                print sname
                sprice = products[j]['skus']['price']
                surl = products[j]['skus']['sUrl']
                sname = products[j]['skus']['alt']
                

                #编码，以便写入文档
                product_id = sid.encode('utf8')
                skuid=skuid1.encode('utf8')
                name = sname.encode('utf8')
                url = surl.encode('utf8')
                price = str(sprice).encode('utf8')
                if skuid!='':
                    data1 = product_id+'-'+skuid+','+url+','+name+','+price+','+label1+','+label2+','+label3+'\n'
                    file_obj1.write(data1)
                else:
                   data1 = product_id+','+url+','+name+','+price+','+label1+','+label2+','+label3+'\n'
                   file_obj1.write(data1)
                   print data1
            file_obj1.close()
            break
        except Exception, e:
            print e
            time.sleep(0.1)
    return True

def getOneCate(cateId):
        label1,label2,label3 = m.getLabel(catId)#调用一个文件，提取标签，返回三个值
        
        for i in xrange(1000):
            print i
            data = 'module=product&from=category&page='+str(i)+'&paramJson=%7B+%22mobile%22+%3A+false+%2C+%22catId%22+%3A+%22cat'+catId+'%22+%2C+%22catalog%22+%3A+%22coo8Store%22+%2C+%22siteId%22+%3A+%22coo8Site%22+%2C+%22shopId%22+%3A+%22%22+%2C+%22regionId%22+%3A+%2211011400%22+%2C+%22pageName%22+%3A+%22list%22+%2C+%22et%22+%3A+%22%22+%2C+%22XSearch%22+%3A+false+%2C+%22startDate%22+%3A+0+%2C+%22endDate%22+%3A+0+%2C+%22pageSize%22+%3A+48+%2C+%22state%22+%3A+4+%2C+%22weight%22+%3A+0+%2C+%22more%22+%3A+0+%2C+%22sale%22+%3A+0+%2C+%22instock%22+%3A+1+%2C+%22filterReqFacets%22+%3A++null++%2C+%22rewriteTag%22+%3A+false+%2C+%22userId%22+%3A+%22%22+%2C+%22priceTag%22+%3A+0%7D'
            res = request_ajax_data(url,data,referer,label1,label2,label3,catId)
            if not res:
                break


if __name__ ==  "__main__": 
    url = 'http://search.gome.com.cn/cloud/asynSearch'
    referer = 'null'
    catIds=['15965733','10000124','10000122']#每一个小类的id
    
    for catId in catIds:
        getOneCate(catId)
