#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
from retrying import retry

class Spider(object):
    def __init__(self):
        self.base_url = 'https://www.br-performance.be/en-be/'
        # if has Chinese, apply decode()
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self.writer_dict = dict()
        self.collect_threads = list()

    @retry
    def get_soup(self, url, timeout=12):
        req=Request(url=url,headers=self.headers)
        html = urlopen(req, timeout=timeout).read().decode('utf-8')
        soup = BeautifulSoup(html, features='lxml')
        return soup

    def get_brand_urls(self):
        brand_urls = list()
        url = "{0}{1}".format(self.base_url, "chiptuning/1-cars/")
        soup = self.get_soup(url)
        items = soup.find_all('a', {"class": "merk"})
        for i in items:
            brand_urls.append(i.get('href'))
        return brand_urls
