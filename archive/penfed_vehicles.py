#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:16:20 2020

@author: ar3
Getting Started with Python Web Scraping

add logging
add logic for additional pages

"""

#
import requests
from urllib3.exceptions import ConnectionError
from bs4 import BeautifulSoup
import sys



#%%
#
def get_html(url):
    header = {
        "From":"Alfredo Ramirez ,<alfram3@gmail.com>"
    }
    
    try:
        response = requests.get(url, headers=header)
    except Exception as err:
        print('(get_html(), Response Exception)')
        print(err)
        sys.exit()
    if response.status_code != 200:
        print("(get_html(), status_code)")
        print("status_code: ", response.status_code)
        print("reason: ", response.reason)
        sys.exit()
    else:
        html = response.text
        return html
       
def vehicle_listings(soup, limit_= None):
    return soup.find_all('div', {'data-qa':'VehicleListing'}, limit=limit_)

def vehicle_listing(vehicle, detail=True):    
    #
    v_data = vehicle_data(vehicle)
    vin = v_data.find('button',{'name':'Save this vehicle'})['data-qa'].replace('save-', '')
    
    listing_url = "https://penfed.truecar.com" + v_data['href']
    year_make_model = v_data.h4.text
    mileage         = v_data.find('div',
                                  {'data-qa':'vehicle-listing-mileage'}).text.replace(',','').replace('miles','').strip()
    mileage = int(mileage)
    distance        = v_data.find('div',
                                  {'data-qa':'vehicle-listing-location'}).text.replace('Distance:', '').strip()
    exterior_colors = v_data.find('div',
                                  {'data-qa':'vehicle-listing-exterior-colors'}).text.replace('Exterior: ', '')
    interior_colors = v_data.find('div',
                                  {'data-qa':'vehicle-listing-interior-colors'}).text.replace('Interior: ', '')
    price_amount    = v_data.find('h4',
                                  {'data-qa':'vehicle-listing-price-amount'}).text.replace('$','').replace(',','')
    price_amount = int(price_amount)
    price_rating    = v_data.find('div',
                                  {'data-qa':'PriceRating'}).text
    vlisting_data = [vin, listing_url, year_make_model, mileage, distance, exterior_colors,
                     interior_colors, price_amount, price_rating]
    if not detail:
        return tuple(vlisting_data)
    
    # vehicle details
    # response = requests.get(listing_url)
    # html = response.text
    html = get_html(listing_url)
    soup = BeautifulSoup(html, 'html.parser')
    vlisting_detail_data = vehicle_details(soup)
    
    return [tuple(vlisting_data), tuple(vlisting_detail_data)]

def vehicle_data(vehicle):
    return vehicle.find('a', {'data-test':'vehicleListingCard'})

def vehicle_details(soup):
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
    mileage = int(mileage)

    # condition history
    condition_history = soup.find('div', {'data-qa':'ConditionHistory'})
    ch_lis = condition_history.find_all('li')
    
    accident_check = ch_lis[0].text
    usage = ch_lis[1].text
    vtitle = ch_lis[2].text
    number_of_owners = ch_lis[3].text
    number_of_owners = int(number_of_owners)

    #
    vehicle_price = soup.find('strong', {'data-test':'vehiclePrice'}).text.replace('$', '').replace(',', '')
    vehicle_price = int(vehicle_price)

    vlisting_detail_data = [exterior_color, style, interior_color, mpg, engine,
                                  transmission, drive_type, fuel_type, mileage, accident_check,
                                  usage, vtitle, number_of_owners, vehicle_price]
    return vlisting_detail_data

def flatten_list(lst):
    new_lst = []
    for itm in lst:
        #print('...', itm)
        new_itm = flatten_item(itm)
        #print('...', new_itm)
        new_lst.append(new_itm)
    return new_lst

def flatten_item(itm):
    flatten_itm = list(itm[0])
    flatten_itm.extend(itm[1])
    #print('...', flatten_itm)
    return tuple(flatten_itm) 

def print_list(collection):
    for n, elem in enumerate(collection):
        print(n)
        print(elem)
        print()
    return None


#%%
listing_keys = ['listing', 
                'year_make_model', 
                'mileage', 
                'distance',
                'exterior_colors', 
                'interior_colors', 
                'price_amount',
                'price_rating']

detail_keys = ['exterior_color',
               'style',
               'interior_color',
               'mpg',
               'engine',
               'transmission',
               'drive_type',
               'fuel_type',
               'milege',
               'accident_check',
               'usage',
               'title',
               'number_of_owners']

# vehicle listings
url = 'https://penfed.truecar.com/used-cars-for-sale/listings/mazda/mx-5-miata/year-2010-max/price-1000-15000/location-san-antonio-tx/?mileageHigh=125000&priceRating[]=well_below_market&priceRating[]=below_market&searchRadius=5000&transmission[]=Automatic'
# response = requests.get(url)
# html = response.text
html = get_html(url)
if not html:
    print('exiting...')
    exit()

soup = BeautifulSoup(html, 'html.parser')

listings = vehicle_listings(soup, limit_=None)

#%%
vehicle_list = []
for vehicle in listings:
    vehicle_list.append(vehicle_listing(vehicle, detail=True))

flat_vehicle_list = flatten_list(vehicle_list)
sorted_vehicle_list = sorted(flat_vehicle_list, key=lambda x: x[-2])   



"""
# import time
# date = time.strftime('%Y%m%d')
"""







