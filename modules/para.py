#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

from modules.generation import Generation

# e.g. "2.0 TS 150hp"
class Para(Generation):
    def __init__(self, brand_url, model_url, generation_url, para_url):
        super(Para, self).__init__(brand_url, model_url, generation_url)
        self.para_url = "{0}{1}".format(self.base_url, para_url)
        self.relative_para_url = para_url
        self.soup = self.get_soup(self.para_url)
        self.power_data = {
            "power_original": [],
            "power_promoted": [],
            "power_diff": [],
        }
        self.torque_data = {
            "torque_original": [],
            "torque_promoted": [],
            "torque_diff": [],
        }
        self.car_info = {
            "brand": [],
            "model": [],
            "generation": [],
            "fuel": [],
            "para": [],
        }
        self.get_power_data()
        self.get_torque_data()
        self.get_car_info()
        self.car_info.update(self.power_data)
        self.car_info.update(self.torque_data)

    def get_car_info(self):
        navigation_bar = self.soup.find('h1', text="Chiptuning").parent
        self.car_info["brand"].append(navigation_bar.find('h3').find('a').get_text())
        self.car_info["model"].append(navigation_bar.find('h4').find('a').get_text())
        try:
            self.car_info["generation"].append('>'.join(navigation_bar.find('h5').find('span').get_text().strip().split()))
        except Exception:
            self.car_info["generation"].append('>'.join(navigation_bar.find('h5').find('a').get_text().strip().split()))
        self.car_info["para"].append(navigation_bar.find('h6').get_text())
        if self.relative_para_url in self.gasoline_urls:
            self.car_info["fuel"].append("Gasoline")
        elif self.relative_para_url in self.diesel_urls:
            self.car_info["fuel"].append("Diesel")

    def get_power_data(self):
        power_data = list()
        items = self.soup.find(text="Power").parent.next_siblings
        for i in items:
            try:
                power_data.append(i.get_text())
            except AttributeError:
                continue
        self.power_data["power_original"].append(power_data[0])
        self.power_data["power_promoted"].append(power_data[1])
        self.power_data["power_diff"].append(power_data[2])

    def get_torque_data(self):
        torque_data = list()
        items = self.soup.find(text="Torque").parent.next_siblings
        for i in items:
            try:
                torque_data.append(i.get_text())
            except AttributeError:
                continue
        self.torque_data["torque_original"].append(torque_data[0])
        self.torque_data["torque_promoted"].append(torque_data[1])
        self.torque_data["torque_diff"].append(torque_data[2])

