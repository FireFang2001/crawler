import os
from time import sleep
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def main():
    base_url = 'http://ac.qq.com'
    driver = webdriver.Chrome()  # 创建Chrome浏览器驱动
    target_url = 'http://ac.qq.com/Comic/comicInfo/id/623537'
    driver.get(target_url)  # 启动浏览器打开页面
    soup = BeautifulSoup(driver.page_source, 'lxml')  # 页面解析
    for a in soup.select('.chapter-page-all a'):
        path = a.attrs['href']
        full_url = urljoin(base_url, path)
        driver.get(full_url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        img_list = soup.select('.comic-contain img')
        #  控制滚动条向下滚动以加载图片
        for i in range(len(img_list)):
            js = "window.scrollTo(0, %d)" % ((i + 1) * 1200)
            driver.execute_script(js)
            sleep(1)  # 若网速慢需加大时间，等待图片加载完成
        soup = BeautifulSoup(driver.page_source, 'lxml')
        img_names_list = os.listdir('./comic/')
        for img in soup.select('.comic-contain img'):
            print(img.attrs['src'])
            img_url = img.attrs['src']
            filename = img_url[img_url.rfind('/&name=') + 1:]
            if filename not in img_names_list:
                try:
                    print(filename)
                    resp = requests.get(img_url)
                    #  保存图片
                    with open('./comic/' + filename, 'wb') as f:
                        f.write(resp.content)
                    print(filename + '下载成功!')
                except OSError:
                    print(filename + '下载失败!')
            else:
                print('图片已存在')
    print('图片下载完成!')


if __name__ == '__main__':
    main()
