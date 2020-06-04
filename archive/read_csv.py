#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:27:26 2020

@author: ar3
"""



# Code generated with CleverCSV version 0.5.5

import clevercsv
import time
import os.path

date = time.strftime('%Y%m%d')
#print(date)

with open("vehicle_urls.txt", "r", newline="", encoding="ascii") as fp:
    reader = clevercsv.reader(fp, delimiter=",", quotechar="\"", escapechar="")
    rows = list(reader)

for row in rows:
    vehicle, url = row
    #print(vehicle, url) ## replace with function call
    html_file = date + "_" + vehicle + ".html"
    #print(html_file, os.path.exists(html_file))
    if os.path.exists(html_file):
        print(html_file + " exists")
        file = open(html_file)
        html = file.read()
        file.close()
        print(html)
    else:
        print(html_file + " not exists")
    

    
