### Scrapy
Scrapy是Python的一个快速、高层次的屏幕抓取和web抓取框架，用于抓取web站点并从页面中提取结构化的数据。Scrapy用途广泛，可以用于数据挖掘、监测和自动化测试，经常被用于网络爬虫开发。
### 怎么使用Scrapy
#### 准备工作
1. 搭建虚拟环境：  
```
python -m venv venv
```
或者用virtualenv
```
pip install virtualenv
virtualenv --no-site-packages venv
```
2. 安装Scrapy:  
先安装依赖库：
到https://www.lfd.uci.edu/~gohlke/pythonlibs  下载Twisted‑18.4.0‑cp36‑cp36m‑win_amd64.whl，36表示python3.6版本，amd64表示64位，需下载对应版本，然后安装
```
pip install PATH/Twisted‑18.4.0‑cp37‑cp37m‑win_amd64.whl
```
PATH为文件路径
```
pip install scrapy
```
如果报错No module named win32api，再安装一个
```
pip install pypiwin32
```
#### 创建Scrapy项目
```
scrapy startproject dushuwang .
scrapy genspider books www.dushu.com
```
Scrapy会创建下列文件：
dushu/  
----dushu/  
--------spiders/  
------------__init__.py  
--------__init__.py  
--------items.py  
--------pipelines.py  
--------settings.py  
----scrapy.cfg  
#### 在PyCharm上配置debug
![avatar](/img/scrapydebug.png)
#### 修改配置文件：settings.py

```python
# -*- coding: utf-8 -*-

# Scrapy settings for douban project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# 配置mongodb，用于数据持久化
MONGODB_SERVER = ''
MONGODB_PORT = 27017
MONGODB_DB = 'dushu'
MONGODB_COLLECTION = 'books'

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'douban.middlewares.DoubanSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'douban.middlewares.DoubanDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'douban.pipelines.DoubanPipeline': 400,
}

LOG_LEVEL = 'DEBUG'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
```
在items.py定义字段，用来保存数据

```python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    auther = scrapy.Field()
    publisher = scrapy.Field()
    price = scrapy.Field()
    book_desc = scrapy.Field()
    auther_desc = scrapy.Field()
    contents = scrapy.Field()
```
在spider目录下写爬虫（本例为spider/books.py文件）
```python
# -*- coding: utf-8 -*-
import scrapy

from dushu.items import BookItem


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/']

    def parse(self, response):
        li_list = response.xpath('/html/body/div[5]/div/div[2]/div[3]/ul/li')
        for li in li_list:
            item = BookItem()
            item['title'] = li.xpath('div/h3/a/text()').extract_first()
            item['auther'] = li.xpath('div/p[1]/a[1]/text()').extract_first()
            href = li.xpath('div/h3/a/@href').extract_first()
            url = response.urljoin(href)
            item['url'] = url
            request = scrapy.Request(url=url, callback=self.parse2)
            request.meta['item'] = item
            yield request

    def parse2(self, response):
        item = response.meta['item']
        item['publisher'] = response.xpath('//*[@id="ctl00_c1_bookleft"]/table/tbody/'
                                           'tr[2]/td[2]/a/text()').extract_first()
        item['price'] = response.xpath('//*[@id="ctl00_c1_bookleft"]/p/span/text()').extract_first()
        item['book_desc'] = response.xpath('//*[@class="book-summary"][1]/div/div/text()').extract_first()
        item['auther_desc'] = response.xpath('//*[@class="book-summary"][2]/div/div/text()').extract_first()
        item['contents'] = response.xpath('//*[@class="book-summary margin-large-bottom"]/div/div/text()').extract()
        return item
```
在pipeline.py里实现数据持久化
```python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class DushuPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.connection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing %s of blogpost from %s' % (data, item['url']))
        item_dict = dict(item)
        if valid:
            new_book = [item_dict]
            self.connection.insert(new_book)
            log.msg("Item wrote to MongoDB database %s/%s" %
                    (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                    level=log.DEBUG, spider=spider)
        return item
```
