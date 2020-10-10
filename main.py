#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
from modules.spider import Spider
from modules.brand import Brand
from modules.model import Model
from modules.generation import Generation
from modules.para import Para
from modules.csv_handler import CsvWriter
from gevent.pool import Pool
from multiprocessing import Process, cpu_count
import os

CPU_COUNT = cpu_count()

def cbrand(spider, group):
    print('Run child process (%s)...' % (os.getpid()))
    pool = Pool(100)
    for brand_url in group:
        brand = Brand(brand_url)
        spider.writer_dict[brand.brand_name] = CsvWriter("~/Documents/{0}.csv".format(brand.brand_name))
        print(brand.brand_name)
        pool.spawn(collect_model, spider, brand)
    pool.join()

def collect_brand(spider):
    print('Parent process (%s).' % os.getpid())
    processes = list()
    brand_urls = spider.get_brand_urls()
    if len(brand_urls) % CPU_COUNT == 0:
        step = int(len(brand_urls) / CPU_COUNT)
    else:
        step = int(len(brand_urls) / CPU_COUNT) + 1

    groups = [brand_urls[i:i + step] for i in range(0, len(brand_urls), step)]

    for group in groups:
        p = Process(target=cbrand, args=(spider, group,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print("Info: collect brand finished!")

def collect_model(spider, brand):
    #print("start collect model")
    pool = Pool(100)
    for model_url in brand.model_urls:
        model = Model(brand.relative_brand_url, model_url)
        pool.spawn(collect_generation, spider, brand, model)
    pool.join()

def collect_generation(spider, brand, model):
    pool = Pool(100)
    for generation_url in model.generation_urls:
        generation = Generation(brand.relative_brand_url, model.relative_model_url, generation_url)
        pool.spawn(collect_car, spider, brand, model, generation)
    pool.join()

def collect_car(spider, brand, model, generation):
    pool = Pool(100)
    #print("start collect car info")
    for para_url in generation.para_urls:
        para = Para(brand.relative_brand_url, model.relative_model_url, generation.relative_generation_url, para_url)
        pool.spawn(write, spider, para, brand)
    pool.join()

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