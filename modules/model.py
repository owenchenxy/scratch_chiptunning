#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
from modules.spider import Spider

class Model(object):
    def __init__(self, model_url):
        # super(Model, self).__init__()
        self.relative_model_url = model_url
        # e.g. chiptuning/1-cars/9-alfa-romeo/79-147/
        self.model_url = "{0}{1}".format(Spider.base_url, model_url)
        self.soup = Spider.get_soup(self.model_url)
        self.generation_urls = list()
        self.get_generation_urls()

    def get_generation_urls(self):
        items = self.soup.find_all('span', {"class": "modelyear"})
        if not items:
            items = self.soup.find_all('article')[1].find('ul').find_all('a')
            for i in items:
                self.generation_urls.append(i.get('href'))
        else:
            for i in items:
                self.generation_urls.append(i.parent.get('href'))

