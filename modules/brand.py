#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

from modules.spider import Spider

class Brand(Spider):
    def __init__(self, brand_url):
        super(Brand, self).__init__()
        self.relative_brand_url = brand_url
        self.brand_url = "{0}{1}".format(self.base_url, brand_url)
        self.soup = self.get_soup(self.brand_url)
        self.model_urls = list()
        self.brand_name = ""
        self.get_model_urls()
        self.get_brand_name()
        
    def get_model_urls(self):
        items = self.soup.find('ul', {"class": "content"}).find_all('a')
        for i in items:
            self.model_urls.append(i.get('href'))

    def get_brand_name(self):
        item = self.soup.find('article').find('h2')
        self.brand_name = item.get_text()