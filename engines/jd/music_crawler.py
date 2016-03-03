# -*- coding: utf-8 -*-

import requests
import re
import time

pattern1 = re.compile(r'http://music\.jd\.com/8_0_desc_\d+.*?\.html')
pattern3 = re.compile(r'<a class="next" href="http://music\.jd\.com/8_0_desc_\d+_1_(\d+)_15.html">末页</a>')
pattern4 = re.compile(r'<a class="next" href="http://music\.jd\.com/3_0_desc_\d+_1_(\d+)_15.html">末页</a>')
pattern5 = re.compile(r'skuid="(\d+)" class="btn btn-follow"')
# pattern3 = re.compile(r'http://music\.jd\.com/8_0_desc_\d+_2_1_15.html')
# pattern4 = re.compile(r'http://music\.jd\.com/8_0_desc_(\d+)_2_1_15.html')
catid_one = []
catid_two = []
productid = []

label1 = '数字商品'
label2 = '数字音乐'
label3 = ''

start_url = 'http://music.jd.com/'

web = requests.get(start_url).content
cat_one = pattern1.findall(web)

file_obj = open('musicid.txt','a')
for each in cat_one:
    try:
        if each not in catid_one:
            catid_one.append(each)
            cat_num = each.split('desc_')[1]
            cat_num = cat_num.split('_')[0]
            if cat_num not in catid_two:
                catid_two.append(cat_num)
            cat_one_web = requests.get(each).content
            pagenum = pattern3.findall(cat_one_web)
            if pagenum:
                pagenum = int(pagenum[0])+1
            else:
                pagenum = 2
            for page in range(1,pagenum):
                url = 'http://music.jd.com/8_0_desc_'+cat_num+'_1_'+str(page)+'_15.html'
                print url
                pagetext = requests.get(url).content
                time.sleep(0.1)
                itemid = pattern5.findall(pagetext)
                if itemid:
                    for every in itemid:
                        if every not in productid:
                            productid.append(every)
                            item = every + ','+'数字商品' + ',' + '数字音乐' + ',' + ''
                            print item
                            file_obj.write(item+'\n')
                else:
                    continue
    except Exception,e:
       error_file = open('error.txt','a')
       error_file.write(each+'\n')
       error_file.close()
       continue

for one in catid_two:
    try:
        two_url = 'http://music.jd.com/3_0_desc_'+one+'_1_1_15.html'
        pageweb = requests.get(two_url).content
        page = pattern4.findall(pageweb)
        if page:
            pagenum = int(pagenum[0])+1
        else:
            pagenum = 2
        for i in range(1,pagenum):
            url = 'http://music.jd.com/3_0_desc_'+one+'_1_'+str(page)+'_15.html'
            print url
            pagetext = requests.get(url).content
            time.sleep(0.1)
            itemid = pattern5.findall(pagetext)
            if itemid:
                for every in itemid:
                    if every not in productid:
                        productid.append(every)
                        item = every + ','+'数字商品' + ',' + '数字音乐' + ',' + ''
                        print item
                        file_obj.write(item+'\n')
            else:
                continue
    except Exception,e:
       error_file = open('error.txt','a')
       error_file.write(one+'\n')
       error_file.close()
       continue

file_obj.close()

