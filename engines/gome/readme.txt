备注version1.0：
吴老师组的国美爬虫代码包括：ajax_crawler.py、catid.py、catid.txt、m.py。
该程序可以继续运行。主程序是ajax_crawl,主程序中用到的catid用catid.py获得
主要就是利用post向服务器发送数据，返回我们所需要的json格式的数据，我们自己再提取。
代码思想就是将三级标签的每一类的id遍历，获得每一个商品信息。

备注version2.0：
新国美爬虫代码gome_crawler.py。
从国美网站首页的全部分类页面进入，抓取每类商品的分类网址，然后分别抓取每类商品。获取商品的id和三个标签。一共抓取443907条商品。