#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

from modules.spider import Spider

class Generation(object):
    def __init__(self, generation_url):
        super(Generation, self).__init__()
        self.relative_generation_url = generation_url
        self.generation_url = "{0}{1}".format(Spider.base_url, generation_url)
        self.soup = Spider.get_soup(self.generation_url)
        self.gasoline_urls = list()
        self.get_gasoline_urls()
        self.diesel_urls = list()
        self.get_diesel_urls()
        self.para_urls = self.gasoline_urls + self.diesel_urls

    def get_gasoline_urls(self):
        try:
            items = self.soup.find(text="Gasoline").parent.parent.next_sibling.next_sibling.find_all('li')
        except Exception:
            return None

        for i in items:
            try:
                self.gasoline_urls.append(i.find('a').get('href'))
            except Exception:
                continue

    def get_diesel_urls(self):
        try:
            items = self.soup.find(text="Diesel").parent.parent.next_sibling.next_sibling.find_all('li')
        except Exception:
            return None

        for i in items:
            try:
                self.diesel_urls.append(i.find('a').get('href'))
            except Exception:
                continue
'''
    def get_generation_name(self):
        item = self.soup.find_all('article')[2].find('span')
        self.generation_name = '>'.join(item.get_text().strip().split())
'''