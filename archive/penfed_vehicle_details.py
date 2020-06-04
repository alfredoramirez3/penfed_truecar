#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:38:16 2020

@author: ar3
"""

#
import requests
from bs4 import BeautifulSoup

#
url = 'https://penfed.truecar.com/used-cars-for-sale/listing/JM1NC2SFXC0222933/2012-mazda-mx-5-miata/'
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

#%%

# vehicle overview
vehicle_overview = soup.find('div', {'data-qa':'vehicle-overview'})

exterior_color = vehicle_overview.find('div', {'data-qa':'vehicle-overview-item-Exterior Color'}).li.text
style = vehicle_overview.find('div', {'data-qa':'vehicle-overview-item-Style'}).li.text
interior_color = vehicle_overview.find('div', {'data-qa':'vehicle-overview-item-Interior Color'}).li.text
mpg = vehicle_overview.find('div', {'data-qa':'vehicle-overview-item-MPG'}).li.text
engine = vehicle_overview.find('div', {'data-qa':'vehicle-overview-item-Engine'}).li.text
transmission = vehicle_overview.find('div', {'data-qa':'vehicle-overview-item-Transmission'}).li.text
drive_type = vehicle_overview.find('div', {'data-qa':'vehicle-overview-item-Drive Type'}).li.text
fuel_type = vehicle_overview.find('div', {'data-qa':'vehicle-overview-item-Fuel Type'}).li.text
mileage = vehicle_overview.find('div', {'data-qa':'vehicle-overview-item-Mileage'}).li.text.replace(',', '')

#%%

# condition history
condition_history = soup.find('div', {'data-qa':'ConditionHistory'})
ch_lis = condition_history.find_all('li')
accident_check = ch_lis[0].text
usage = ch_lis[1].text
vtitle = ch_lis[2].text
number_of_owners = ch_lis[3].text

#%%
#
vehicle_price = soup.find('strong', {'data-test':'vehiclePrice'}).text.replace('$', '').replace(',', '')






