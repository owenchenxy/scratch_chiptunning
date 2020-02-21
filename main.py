#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
from modules.spider import Spider
from modules.brand import Brand
from modules.model import Model
from modules.generation import Generation
from modules.para import Para
from modules.csv_handler import CsvWriter
from threading import Thread

def collect_brand(spider):
    threads = list()
    brand_urls = spider.get_brand_urls()
    count = 0
    for brand_url in brand_urls:
        count += 1
        brand = Brand(brand_url)
        spider.writer_dict[brand.brand_name] = CsvWriter("/Users/xianyaochen/Documents/{0}.csv".format(brand.brand_name))
        t = Thread(target=collect_model, args=(spider, brand,))
        t.start()
        threads.append(t)
    print("Info: Collecting {0} brands car info ...".format(count))
    for t in threads:
        t.join()
    print("Info: collect brand finished!")

def collect_model(spider, brand):
    #print("start collect model")
    for model_url in brand.model_urls:
        model = Model(brand.relative_brand_url, model_url)
        t = Thread(target=collect_generation, args=(spider, brand, model))
        t.start()

def collect_generation(spider, brand, model):
    for generation_url in model.generation_urls:
        generation = Generation(brand.relative_brand_url, model.relative_model_url, generation_url)
        t = Thread(target=collect_car, args=(spider, brand, model, generation))
        t.start()

def collect_car(spider, brand, model, generation):
    #print("start collect car info")
    for para_url in generation.para_urls:
        para = Para(brand.relative_brand_url, model.relative_model_url, generation.relative_generation_url, para_url)
        t = Thread(target=write, args=(spider, para, brand))
        t.start()

def write(spider, para, brand):
    #print("start write csv file")
    spider.writer_dict[brand.brand_name].write_to_csv(para.car_info)

def sort_result(spider):
    count = 0
    for brand_name, brand_writer in spider.writer_dict.items():
        brand_writer.sort_csv()
        count += 1
    print("Info: {0} files have been sorted!")


def main():
    spider = Spider()
    collect_brand(spider)
    sort_result(spider)

if __name__ == "__main__":
    main()