#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 13:06:55 2020

@author: ar3
"""

#
import sys
import general_webscraping as gws
import application_webscraping as aws


#
date = gws.date()

def get_vehicles_from_main_listing_pages(make_model, starting_url):
    # get vehicles from main listing page(s) 
    page_url = starting_url
    page = 0
    vehicles = []
    while page_url:
        page += 1
        
        # uncomment to save html main page(s)
        html_filename = aws.get_html_filename(date, make_model, page)
        html = gws.get_html(page_url, html_filename)
 
        if html is None:
            return [], []
    
        #####                                        note limit ===> #
        next_page_url, listings = aws.extract_listings(html, limit_=None)
        
        vehicles.extend(listings)    
        page_url = next_page_url 
        
    return vehicles

def get_vehicle_details(vehicles):
    details = aws.extract_vehicle_details(vehicles)
    return details    
    
def get_vehicle_list(vehicles, vehicle_details):
    vehicle_list = []
    if vehicles and vehicle_details:
        vehicle_list = list(zip(vehicles, vehicle_details))
        vehicle_list = gws.flatten_list(vehicle_list)
    return vehicle_list

#    
def main(arg1, arg2):
    make_model = arg1
    starting_url = arg2

    # get the listings (vehicles) from the main pages
    vehicles = get_vehicles_from_main_listing_pages(make_model, starting_url)
    
    # for each of the vehicles follow the detail page url and get details
    vehicle_details = get_vehicle_details(vehicles)    

    # combine the the tuple(vehicle, vehicle_details) into a flattened tuple
    vehicle_list = get_vehicle_list(vehicles, vehicle_details)
    
    # save the vehicle_list as a csv file
    csv_filename = aws.get_csv_filename(date, make_model)
    
    headers = aws.get_listings_headers()
    headers.extend(aws.get_vehicle_details_headers())
    
    gws.write_csv(csv_filename, headers, vehicle_list)
    
    return headers, vehicle_list # remove this return of list? 

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
