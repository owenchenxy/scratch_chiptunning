#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

from multiprocessing import cpu_count, RLock
from modules.spider import Spider

lock = RLock()
CPU_COUNT = cpu_count() - 1
spider = Spider()