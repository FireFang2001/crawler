import logging
import pickle
import zlib
from hashlib import sha1

import pymongo
from enum import Enum, unique
# from queue import Queue
from random import random
from threading import Thread, current_thread
from time import sleep
from urllib.parse import urlparse

import redis
import requests
from bs4 import BeautifulSoup
from bson import Binary


def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            pass
            # logging.error('Decode:', error)
    return page_html


@unique
class SpiderStatus(Enum):
    """
    ‘蜘蛛’的状态
    """
    IDLE = 0
    WORKING = 1


class Retry(object):
    def __init__(self, *, retry_times=3, wait_secs=5, errors=(Exception,)):
        self.retry_times = retry_times
        self.wait_secs = wait_secs
        self.errors = errors

    def __call__(self, fn):

        def wrapper(*args, **kwargs):
            for _ in range(self.retry_times):
                try:
                    return fn(*args, **kwargs)
                except self.errors as e:
                    logging.error(e)
                    logging.info('......')
                    sleep((random() + 1) * self.wait_secs)
            return None

        return wrapper


class Spider(object):
    """
    爬虫对象
    """
    def __init__(self):
        self.status = SpiderStatus.IDLE

    @Retry()
    def fetch(self, current_url, *, charsets=('utf-8',), user_agent=None, proxies=None):
        """
        抓取页面
        :param current_url:
        :param charsets:
        :param user_agent:
        :param proxies:
        :return:
        """
        logging.info('[Fetch]: ' + current_url)
        thread_name = current_thread().name
        print(f'[{thread_name}]: {current_url}')
        headers = {'user-agent': user_agent} if user_agent else {}
        resp = requests.get(current_url, headers=headers, proxies=proxies)
        return decode_page(resp.content, charsets) if resp.status_code == 200 else None

    def parse(self, html_page, *, domain='m.sohu.com'):
        """
        解析页面
        :param html_page:
        :param domain:
        :return:
        """
        soup = BeautifulSoup(html_page, 'lxml')
        for a in soup.body.select('a[href]'):
            parser = urlparse(a.attrs['href'])
            scheme = parser.scheme or 'http'
            netloc = parser.netloc or domain
            if scheme != 'javascript' and netloc == domain:
                path = parser.path
                query = '?' + parser.query if parser.query else ''
                full_url = f'{scheme}://{netloc}{path}{query}'
                if not redis_client.sismember('visited_urls', full_url):
                    redis_client.rpush('m_sohu_tasks', full_url)

    def extract(self, html_page):
        pass

    def store(self, data_dict):
        pass


# Thread(target=foo, args=(,)).start()
class SpiderThread(Thread):
    """
    线程对象
    """
    def __init__(self, spider, name):
        super().__init__(daemon=True)
        self.spider = spider
        self.name = name

    def run(self):
        while True:
            current_url = redis_client.lpop('m_sohu_tasks')  # 从队列中获取url
            while not current_url:
                current_url = redis_client.lpop('m_sohu_tasks')
            current_url = current_url.decode('utf-8')
            self.spider.status = SpiderStatus.WORKING  # 改变spider状态到WORKING
            html_page = self.spider.fetch(current_url)  # spider获取页面
            redis_client.sadd('visited_urls', current_url)
            if html_page not in [None, '']:
                hasher = hasher_proto.copy()
                hasher.update(current_url.encode('utf-8'))
                doc_id = hasher.hexdigest()
                if not sohu_data_coll.find_one({'_id': doc_id}):
                    sohu_data_coll.insert_one({'_id': doc_id,
                                               'url': current_url,
                                               'page': Binary(zlib.compress(pickle.dumps(html_page)))})
                self.spider.parse(html_page)  # 解析页面获得url列表
            self.spider.status = SpiderStatus.IDLE  # spider状态改为IDLE


def is_any_alive(spider_threads):
    """
    判断线程队列状态
    :param spider_threads:
    :return: 所有蜘蛛停止，返回False；否则返回True
    """
    return any([spider_thread.spider.status == SpiderStatus.WORKING
                for spider_thread in spider_threads])


redis_client = redis.Redis(host='101.132.164.252', port=6379, password='root')
mongo_client = pymongo.MongoClient(host='47.98.56.23', port=27017)
sohu_data_coll = mongo_client.msohu.webpages
hasher_proto = sha1()


def main():
    # task_queue = Queue()  # 队列，先进先出
    if not redis_client.exists('m_sohu_tasks'):
        redis_client.rpush('m_sohu_tasks', 'http://m.sohu.com/')
    # task_queue.put('http://m.sohu.com/')
    #  创建线程对象
    spider_threads = [SpiderThread(Spider(), 'thread-%d' % i)
                      for i in range(10)]
    #  开始执行线程
    for spider_thread in spider_threads:
        spider_thread.start()
    # 有任务或有至少一个蜘蛛活着，程序继续
    while redis_client.llen('m_sohu_tasks') != 0 or is_any_alive(spider_threads):
        pass
    print('执行结束')


if __name__ == '__main__':
    main()
