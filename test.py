#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

import pandas as pd

data = pd.read_csv("/Users/xianyaochen/Documents/tuning.csv")
data.sort_values(by='brand', ascending=False, inplace=True)
data.to_csv("/Users/xianyaochen/Documents/tuning.csv", index=False)
