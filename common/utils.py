#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

from gevent import monkey
from gevent.pool import Pool
from common.constants import CPU_COUNT, spider, lock
from modules.brand import Brand
from modules.model import Model
from modules.generation import Generation
from modules.para import Para
from modules.csv_handler import CsvWriter
from multiprocessing import Process
import os
from importlib import reload
import socket

def cbrand(group):
    print('Run child process (%s)...' % (os.getpid()))
    pool = Pool(100)
    for brand_url in group:
        brand = Brand(brand_url)
        with lock:
            reload(socket)
            spider.writer_dict[brand.brand_name] = CsvWriter("/root/docs/{0}.csv".format(brand.brand_name))
            monkey.patch_socket()
        pool.spawn(collect_model, brand)
    pool.join()

def collect_brand():
    print('Parent process (%s).' % os.getpid())
    processes = list()
    brand_urls = spider.get_brand_urls()

    # 给brand绑cpu
    groups = [[] for _ in range(CPU_COUNT)]
    [groups[i%CPU_COUNT].append(brand_urls[i]) for i in range(len(brand_urls))]

    # 每个cpu负责爬取一组brand
    for group in groups:
        p = Process(target=cbrand, args=(group,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print("Info: collect brand finished!")

def collect_model(brand):
    #print("start collect model")
    pool = Pool(100)
    for model_url in brand.model_urls:
        model = Model(model_url)
        pool.spawn(collect_generation, brand, model)
    pool.join()

def collect_generation(brand, model):
    pool = Pool(100)
    for generation_url in model.generation_urls:
        generation = Generation(generation_url)
        pool.spawn(collect_car, brand, model, generation)
    pool.join()

def collect_car(brand, model, generation):
    pool = Pool(100)
    #print("start collect car info")
    for para_url in generation.para_urls:
        para = Para(generation.relative_generation_url, para_url)
        pool.spawn(write, para, brand)
    pool.join()

def write(para, brand):
    #print("start write csv file")
    spider.writer_dict[brand.brand_name].write_to_csv(para.car_info)
    del para

def sort_result():
    count = 0
    with lock:
        reload(socket)
        for brand_name, brand_writer in spider.writer_dict.items():
            brand_writer.sort_csv()
            count += 1
        monkey.patch_socket()
    print("Info: {0} files have been sorted!".format(count))
