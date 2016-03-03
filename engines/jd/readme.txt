备注version1.0：
jd0.txt+jd.py是吴老师组写的爬虫。
现在代码可能不适用京东的网站，但是思想还是差不多的。
通过京东的分类页的url规律进入商品界面获取商品信息。
jd0.txt里面代表的jd的三级标签的url.

备注version2.0：
jd_spider_ver3.py是用scrapy框架写的京东商品爬虫。从京东的全部分类页面进入抓取每个分类下的商品。共抓取7908135个商品。
个别商品类未被jd_spider_ver3.py抓取到。pet_crawler.py、ebook_crawler.py、mvd_crawler.py也是用scrapy框架写的。music_crawler.py是用普通python写的。
music_crawler.py补取数字音乐类商品45309条，mvd_crawler.py补抓音像类商品464264条，pet_crawler.py补抓宠物类商品142309条，ebook_crawler.py补抓电子书商品类80794条。
共抓取8640811条京东商品。


