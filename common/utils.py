#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

from gevent.pool import Pool
from common.constants import CPU_COUNT, DATA_Q
from modules.csv_handler import CsvWriter
from modules.brand import Brand
from modules.model import Model
from modules.generation import Generation
from modules.para import Para
from multiprocessing import Process
import os
from modules.spider import Spider
import time

global COLLECT_DONE
COLLECT_DONE = False

def collect_brand(group):
    print('Run child process (%s)...' % (os.getpid()))
    pool = Pool(100)
    for brand_url in group:
        brand = Brand(brand_url)
        pool.spawn(collect_model, brand)
    pool.join()

def start_collect():
    print('Parent process (%s).' % os.getpid())
    processes = list()
    brand_urls = Spider.get_brand_urls()

    # 给brand绑cpu
    groups = [[] for _ in range(CPU_COUNT)]
    [groups[i%CPU_COUNT].append(brand_urls[i]) for i in range(len(brand_urls))]

    # 每个cpu负责爬取一组brand
    for group in groups:
        p = Process(target=collect_brand, args=(group,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    global COLLECT_DONE
    COLLECT_DONE = True
    print("Info: collect brand finished!")

def collect_model(brand):
    #print("start collect model")
    pool = Pool(100)
    for model_url in brand.model_urls:
        model = Model(model_url)
        pool.spawn(collect_generation, model)
    pool.join()

def collect_generation(model):
    pool = Pool(100)
    for generation_url in model.generation_urls:
        generation = Generation(generation_url)
        pool.spawn(collect_car, generation)
    pool.join()

def collect_car(generation):
    pool = Pool(100)
    paras = []
    for para_url in generation.para_urls:
        para = Para(generation.relative_generation_url, para_url)
        paras.append(para)
        pool.spawn(push, para)
    pool.join()

def push(para):
    DATA_Q.put(para.car_info)

def write(dir):
    w = CsvWriter(dir)
    global COLLECT_DONE
    while not COLLECT_DONE or not DATA_Q.empty():
        if COLLECT_DONE and not DATA_Q.empty():
            print("Q is not empty")
        try:
            data = DATA_Q.get(block=False)
        except Exception:
            time.sleep(0.01)
            continue
        w.write_to_csv(data)

    # 收集数据的子进程结束后，且数据队列取完后，对结果进行排序
    w.sort_csv()

def start_writer(dir):
    pool = Pool(1)
    pool.spawn(write, dir)
    return pool

