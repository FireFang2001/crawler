### Scrapy
Scrapy是Python的一个快速、高层次的屏幕抓取和web抓取框架，用于抓取web站点并从页面中提取结构化的数据。Scrapy用途广泛，可以用于数据挖掘、监测和自动化测试，经常被用于网络爬虫开发。
#### 怎么使用Scrapy
##### 准备工作
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
