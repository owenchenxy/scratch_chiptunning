#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all(thread=False)

import cProfile
from common.utils import collect_brand, sort_result

def main():
    collect_brand()
    sort_result()

if __name__ == "__main__":
    # main()
    print(cProfile.run('main()'))