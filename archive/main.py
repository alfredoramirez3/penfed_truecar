#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:27:26 2020

@author: ar3
"""


#
def get_urls(filename):
    with open(filename, "r", newline="", encoding="ascii") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar="\"", escapechar="")
        rows = list(reader)   
    return rows

def get_html(url, html_file=None):
    
    
    if html_file and os.path.exists(html_file):
        file = open(html_file)
        html = file.read()
        file.close()
        return html

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
        if html and html_file:
            write_html(html_file,html)       
        return html

def write_html(filename, html):
    file = open(filename, "w")
    file.write(html)
    file.close()
    return None

def vehicle_listings(soup, limit_= None): 
    #return soup.find_all('div', {'data-qa':'VehicleListing'}, limit=limit_)
    # 2/20/2020
    #<div data-qa="Listings" ...</div> 
    return soup.find_all('div', {'data-qa':'Listings'}, limit=limit_)

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

def next_page_url(soup):
    url = soup.find('a', {'class':'page-link'})['href']
    return url
    
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

def write_csv(filename, headers, vehicles):
    df = pd.DataFrame(vehicles)
    df.to_csv(filename, header=headers)
    return

#import clevercsv
import csv
import time
import os.path

import requests
#from urllib3.exceptions import ConnectionError
from bs4 import BeautifulSoup
import sys

import pandas as pd
import copy

listing_keys = ['vin',
                'listing_url', 
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
               'dmilege',
               'accident_check',
               'usage',
               'title',
               'number_of_owners',
               'vehicle_price']

headers = copy.copy(listing_keys)
headers.extend(detail_keys)



date = time.strftime('%Y%m%d')
#print(date)

input_rows = get_urls("./input/make-model_urls.txt")
for row in [row for row in input_rows if row[0].lower() == "true"]:
    _, make_model, url = row
    #print(vehicle_make_model, url)
    
    page_url = url
    page = 0
    while page_url:
        page += 1
        html_file = "./html/"+ date + "_" + make_model + "_page" +str(page) + ".html"
        csv_filename = "./output/" + date + "_" + make_model + ".csv"
        html = get_html(page_url) #, html_file)
 
        if not html:
            print('exiting...')
            exit()
    
        #soup = BeautifulSoup(html, 'html.parser')
        soup = BeautifulSoup(html, 'html5lib')
        listings = vehicle_listings(soup, limit_=None)
        
        vehicles = []
        for vehicle in listings:
            vehicles.append(vehicle_listing(vehicle, detail=True))
            
        page_url = next_page_url(soup)
        page_url = "https://penfed.truecar.com/" + page_url
            
    # write to csv
    flat_vehicles = flatten_list(vehicles)
    write_csv(csv_filename, headers, flat_vehicles)




