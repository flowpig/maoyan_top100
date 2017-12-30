#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from requests.exceptions import RequestException
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import re
import json


def get_one_page(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>'
        + '.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?score"><i.*?>(.*?)</i><i.*?>(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4][5:],
            'score':item[5] + item[6]
        }

def write_to_file(content):
    with open('maoyan_top100','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()


def spider_crawl(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = get_one_page(url, headers)
    # print(html)
    items = parse_one_page(html)
    for item in items:
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    # # 多进程进程池爬取 multiprocessing    (乱序的)
    # pool = Pool()
    # pool.map(spider_crawl,[i*10 for i in range(10)])

    #线程池爬取  concurrent.futures     (乱序的)
    pool = ThreadPoolExecutor()
    pool.map(spider_crawl,[i*10 for i in range(10)])
    # 使用map更加方便
    # for i in range(10):
    #     pool.submit(spider_crawl,i*10)
    # pool.shutdown(wait=True)

    #普通爬取
    # for i in range(10):
    #     spider_crawl(i*10)
