import requests
from lxml import etree
res=requests.get('http://list.gome.com.cn/')
data=res.content
data1=etree.HTML(data.decode('utf8'))
url=data1.xpath("//div[@class='in']/a//@href")
len_1= len(url)
file_obj=open('catid.txt','a+')

for i in xrange(len_1):
    
    #print url[i][27:35]
    file_obj.write(url[i][27:35]+'\n')
file_obj.close()
    
