#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 13:06:55 2020

@author: ar3

#    TODO:
#        0. add price_rating value from detail!:
#        <span class="graph-icon-title margin-left-1">Great Price</span>
#        
#        1. add time column to csv output:          DONE
#        2. add time delay between detail calls:    under study       
#        3. add logging:                            under study
#        4. add either email or sms notification:   under study
#        5. add copy csv files to dropbox:          no progress
#        6. create cron jobs for nightly execution:  no progress
            a. execute webscraping
            b. copy csv files to dropbox
            c. send email or sms text
"""
#
import application_webscraping as aws
import penfed_truecar as pf

#
print('processing started')
input_rows = aws.get_urls()
for row in [row for row in input_rows if row[0].lower() == "true"]:
    _, make_model, start_url = row
    headers, vehicle_list = pf.main(make_model, start_url)
    
    if vehicle_list is not []:
        print(make_model, str(len(vehicle_list)))
    else:
        print(make_model, " extraction failed")
        
print('processing completed')
