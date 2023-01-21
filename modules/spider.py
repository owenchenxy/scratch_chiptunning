#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen,Request

class Spider(object):
    base_url = 'https://www.br-performance.be/en-be/'
    # if has Chinese, apply decode()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    @staticmethod
    def get_soup(url, timeout=10):
        count = 10
        while count > 0:
            try:
                req=Request(url=url,headers=Spider.headers)
                html = urlopen(req, timeout=timeout).read().decode('utf-8')
                soup = BeautifulSoup(html, features='lxml')
                return soup
            except Exception:
                count -= 1
        raise

    @staticmethod
    def get_brand_urls():
        brand_urls = list()
        url = "{0}{1}".format(Spider.base_url, "chiptuning/1-cars/")
        soup = Spider.get_soup(url)
        items = soup.find_all('a', {"class": "merk"})
        for i in items:
            brand_urls.append(i.get('href'))
        return brand_urls
