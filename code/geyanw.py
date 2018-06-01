from hashlib import sha1

import pymongo
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def main():
    mongo_client = pymongo.MongoClient(host=xxxx, port=xxxx)  # 建立mongodb客户端
    geyanw_data_coll = mongo_client.geyanw.webpages
    hasher_proto = sha1()
    base_url = 'https://www.geyanw.com/'
    resp = requests.get(base_url)
    soup = BeautifulSoup(resp.content.decode('gb2312'), 'lxml')
    for dl in soup.select('.tbox'):
        path_list = [a.attrs['href'] for a in dl.select('li a')]
        counter = 0
        title = dl.strong.text
        title_url = dl.dt.a.attrs['href']
        hasher = hasher_proto.copy()
        hasher.update(title_url.encode('utf-8'))
        doc_id = hasher.hexdigest()  # 将连接转为hash值并作为_id值
        if not geyanw_data_coll.find_one({'_id': doc_id}):  # 判断是否已经爬取
            # 将爬取的连接标题存入mongodb
            geyanw_data_coll.insert_one({
                '_id': doc_id,
                'title': title,
                'path': title_url,
            })
        for path in path_list:
            counter += 1
            page = 'page%d' % counter
            full_path = urljoin(base_url, path)
            resp = requests.get(full_path)
            soup = BeautifulSoup(resp.content, 'lxml')
            sec_title = soup.title.text
            current_url = full_path
            content = ''
            for p in soup.select('.content p'):
                if len(p.text) > 2:  # 排除空行
                    content += p.text
            geyanw_data_coll.update({'_id': doc_id}, {'$set': {page: {
                'title': sec_title,
                'url': current_url,
                'content': content
            }}})


if __name__ == '__main__':
    main()
