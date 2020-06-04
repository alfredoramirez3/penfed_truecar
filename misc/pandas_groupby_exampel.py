#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 10:10:24 2020

@author: ar3
"""
import pandas

df = pandas.DataFrame({
    'grp': ['a', 'a', 'b', 'b', 'b', 'c', 'c', 'c', 'd', 'd',],
    'val': [  5,  10,  16,  20,  30,  45, 100, 200, 250, 500,]})

diff = df.groupby('grp')['val'].rolling(2).apply(lambda val: val[1] -val[0], raw=True)
#diff.reset_index(drop=True, inplace=True)
#diff = diff.to_frame('price_diff')

#df = df.join(diff)