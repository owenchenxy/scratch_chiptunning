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
        for i in self.soup.find('ul', {"class": "content"}).find_all('a'):
            self.model_urls.append(i.get('href'))

    def get_brand_name(self):
        self.brand_name = self.soup.find('article').find('h2').get_text()