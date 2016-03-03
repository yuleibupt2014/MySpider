# -*- coding: utf-8 -*-
import os
import time
import socket
import re
import glob
import urllib2

def getLabel(a):

    for i in xrange(2):
        try:
            #打开我网页
            datalable = urllib2.urlopen('http://www.gome.com.cn/category/cat'+a+'.html ').readlines()
            for line in datalable:
               pattern2=re.compile(r'.*?var catMap =".*?:.*?:.*?";')#正则表达式1
               match2=pattern2.match(line)#第一个表达式和读取的a比较
               if match2:
                   data2=match2.group()
                   print 'ok'
                   print a
                   labelbegin=data2.find('"')
                   #print labelbegin
                   labelend=data2.find(';',labelbegin)
                   #print labelend
                   labelall=data2[labelbegin+1:labelend-1]
                   #提取的标签是label1:label2:label3的格式，将三个label分开
                   label=labelall.split(':')

                   print label[0]
                   return label[0],label[1],label[2]
        except Exception, e:
            print e
