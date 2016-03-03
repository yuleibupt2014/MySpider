# -*- coding: utf-8 -*-
import requests
import re
import time
id_set = set()
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
def parse_webpage(url,data,referer,label1,label2,label3, catid):
        for i in xrange(2):
            try:
                res = requests.post(url, data=data, headers=headers)
                if res.status_code != 200 or res.content is "":
                    continue
                obj_json = res.json()
                products = obj_json['products']
                n=len(products)
                if n is 0:
                    return False

                for j in xrange(n):
                    sid = products[j]['pId']#在json表里提取需要的信息
                    skuid1=products[j]['skuId']
                    product_id = sid.encode('utf8')
                    skuid=skuid1.encode('utf8')
                    if skuid!='':
                        product = product_id+'-'+skuid
                        data1 = label1+','+label2+','+label3+','+product_id+'-'+skuid+'\n'
                        if product not in id_set:
                            id_set.add(product)
                            file_obj1.write(data1)
                    else:
                        data1 = label1+','+label2+','+label3+','+product_id+'\n'
                        if product_id not in id_set:
                            id_set.add(product)
                            file_obj1.write(data1)
            except Exception, e:
                print e
                time.sleep(0.1)
        return True

def getInfo(one):
    openurl = 'http://list.gome.com.cn/cat'+one+'.html'
    webtext = requests.get(openurl).content
    pattern1 = re.compile(r'var dsp_gome_c1name = "(.*?)";')
    pattern2 = re.compile(r'var dsp_gome_c2name = "(.*?)";')
    pattern3 = re.compile(r'var dsp_gome_c3name = "(.*?)";')
    pattern4 = re.compile(r'data-totalPageNum="(\d+)"')
    lab1 = pattern1.findall(webtext)[0]
    lab2 = pattern2.findall(webtext)[0]
    lab3 = pattern3.findall(webtext)[0]
    totalpage = pattern4.findall(webtext)
    if totalpage:
        totalpage = totalpage[0]
    else:
        totalpage = 1
    return lab1,lab2,lab3,totalpage

def getOneCate(onecat):
        label1,label2,label3,pagenum = getInfo(onecat)
        pagenumber = int(pagenum)+3
        for i in xrange(pagenumber):
            print onecat,'page = ',i
            time.sleep(0.1)
            data = 'module=product&from=category&page='+str(i)+'&paramJson=%7B+%22mobile%22+%3A+false+%2C+%22catId%22+%3A+%22cat'+onecat+'%22+%2C+%22catalog%22+%3A+%22coo8Store%22+%2C+%22siteId%22+%3A+%22coo8Site%22+%2C+%22shopId%22+%3A+%22%22+%2C+%22regionId%22+%3A+%2211011400%22+%2C+%22pageName%22+%3A+%22list%22+%2C+%22et%22+%3A+%22%22+%2C+%22XSearch%22+%3A+false+%2C+%22startDate%22+%3A+0+%2C+%22endDate%22+%3A+0+%2C+%22pageSize%22+%3A+48+%2C+%22state%22+%3A+4+%2C+%22weight%22+%3A+0+%2C+%22more%22+%3A+0+%2C+%22sale%22+%3A+0+%2C+%22instock%22+%3A+1+%2C+%22filterReqFacets%22+%3A++null++%2C+%22rewriteTag%22+%3A+false+%2C+%22userId%22+%3A+%22%22+%2C+%22priceTag%22+%3A+0%7D'
            res = parse_webpage(url,data,referer,label1,label2,label3,onecat)
            if not res:
                break

def parsecat(url):
    web = requests.get(url).content
    pattern = re.compile(r'http://list.gome.com.cn/cat\d+\.html')
    caturl = pattern.findall(web)
    catnumber = []
    for each in caturl:
        temp = each.split('cat')[1]
        temp = temp.split('.html')[0]
        catnumber.append(temp)
    return   catnumber

if __name__ ==  "__main__":
    start_url = 'http://list.gome.com.cn/'
    catID = parsecat(start_url)
    url = 'http://search.gome.com.cn/cloud/asynSearch'
    referer = 'null'
    file_obj1=open("gome_id.txt" ,'a+')
    for one in catID:
        getOneCate(one)
    file_obj1.close()
