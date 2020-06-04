#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 13:54:31 2020

@author: ar3
"""


listings = soup.find_all('div', {'data-qa':'VehicleListing'})

len(listings)
Out[123]: 30


url = 'https://penfed.truecar.com/used-cars-for-sale/listings/mazda/mx-5-miata/price-below-15000/location-san-antonio-tx/?mileageHigh=125000&priceRating[]=well_below_market&priceRating[]=below_market&searchRadius=5000'
import requests
from bs4 import BeautifulSoup
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
soup
soup.find('div', {'data-qa':'Listings'})
listings = soup.find('div', {'data-qa':'Listings'})
len(soup.find_all('div', {'data-qa':'Listings'}))
listings = soup.find('div', {'data-test':'llVehicleListings'})
listings
listings = soup.find('div', {'data-test':'allVehicleListings'})
listings
all_listings = listings
all_listings
len(all_listings.find_all('div', {'data-qa':'Listings'}))
len(soup.find_all('div', {'data-qa':'Listings'}))
soup = BeautifulSoup(html, 'html5lib')
len(soup.find_all('div', {'data-qa':'Listings'}))
def div_and_dataqa(tag):
    return tag.name='div' and tag.has_attr('data-qa')
def div_and_dataqa(tag):
    return tag.name=='div' and tag.has_attr('data-qa')
    
soup.find_all(div_and_dataqa)
def div_and_dataqa(tag):
    return tag.name=='div' and tag.has_attr('data-qa')
    
soup.find_all(div_and_qa)
soup.find_all(div_and_dataqa)
n, t in enumerate(soup.find_all(div_and_dataqa))
for n, t in enumerate(soup.find_all(div_and_dataqa)):
    if t['data-qa'] == 'Listings':
        print(n)
        print(tag)
        print()
        
for n, t in enumerate(soup.find_all(div_and_dataqa)):
    if t['data-qa'] == 'Listings':
        print(n)
        print(t)
        print()
        
for n, t in enumerate(soup.find_all(div_and_dataqa)):
    if t['data-qa'] == 'Listings':
        print(n)
        #print(t)
        print()
        
for n, t in enumerate(soup.find_all(div_and_dataqa)):
    if t['data-qa'] == 'CardContent':
        print(n)
        #print(t)
        print()
        
for n, t in enumerate(soup.find_all(div_and_dataqa)):
    if t['data-qa'] == 'CardContent':
        print(n)
        #print(t)
        print()
        
for n, t in enumerate(soup.find_all(div_and_dataqa)):
    print(t.name, t['data-qa'])
    print(n)
    #print(t)
    print()
    
for n, t in enumerate(soup.find_all(div_and_dataqa)):
    if t['data-qa'] == 'VehicleListing':
        print(t.name, t['data-qa'])
        print(n)
        #print(t)
        print()
        
soup.find_all('div', {'data-qa':'VehicleListing'})
len(soup.find_all('div', {'data-qa':'VehicleListing'}))
listings = soup.find_all('div', {'data-qa':'VehicleListing'})
len(listings)
listing[0]
listings[0]
print(listings[0].prettify())
listings[0].find('span', {'class':'vehicle-card-year'})
soup.find_all('a', {'data-test':'vehicleListingCard'})
len(soup.find_all('a', {'data-test':'vehicleListingCard'}))
soup.find('a', {'data-test':'vehicleListingCard'})
print(soup.find('a', {'data-test':'vehicleListingCard'}).prettify)
print(soup.find('a', {'data-test':'vehicleListingCard'}).prettify())
#####

"""
new element specs as of 2/20/2020
"""
# setup
url = 'https://penfed.truecar.com/used-cars-for-sale/listings/mazda/mx-5-miata/price-below-15000/location-san-antonio-tx/?mileageHigh=125000&priceRating[]=well_below_market&priceRating[]=below_market&searchRadius=5000'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html5lib')

# vehicle info
len(soup.find_all('div', {'data-qa':'Listings'}))
Out[34]: 30

listings = soup.find_all('div', {'data-qa':'Listings'})

listing0 = listing[0]

listing0.find('span', {'class':'vehicle-card-year'}).text
Out[41]: '2014'

listing0.find('span', {'class':'vehicle-header-make-model'}).text
Out[44]: 'Mazda MX-5 Miata'

listing0.find('div', {'data-test':'vehicleCardTrim'}).text
Out[46]: 'Club Automatic'

listing0.find('span', {'class':'vehicle-card-price-rating-label'}).text
Out[49]: 'Great Price'

listing0.find('h4', {'data-test':'vehicleCardPricingBlockPrice'}).text
Out[51]: '$14,951'

listing0.find('svg', {'data-qa':'IconSpeedometer'}).parent.text
Out[54]: '11,840 miles'

listing0.find('div', {'data-test':'vehicleCardLocation'}).text
Out[56]: '9.8 mi - San Antonio, TX'

listing0.find('div', {'data-test':'vehicleCardColors'}).text
Out[58]: 'Red exterior, Black interior'

listing0.find('div', {'data-test':'vehicleCardCondition'}).text
Out[60]: '1 accident, 2 Owners, Personal use'


#<a data-qa="Pagination-directional-next" data-test="Pagination-directional-next" class="page-link" href="/used-cars-for-sale/listings/mazda/mx-5-miata/year-2010-max/price-below-15000/location-san-antonio-tx/?mileageHigh=125000&amp;page=2&amp;priceRating[]=well_below_market&amp;priceRating[]=below_market&amp;priceRating[]=at_market&amp;searchRadius=5000&amp;transmission[]=Automatic"><svg viewBox="0 0 24 24" class="icon icon-color-default" style="width: 24px; height: 24px; stroke-width: 1px;" data-qa="IconAngleRight"><path d="M9.37 7.17l5.1 5.1-5.1 5.11"></path></svg></a>
soup.find("a", {"data-qa":"Pagination-directional-next"})["href"]
Out[34]: '/used-cars-for-sale/listings/mazda/mx-5-miata/year-2010-max/price-below-15000/?mileageHigh=125000&page=2&priceRating[]=well_below_market&priceRating[]=below_market&priceRating[]=at_market&searchRadius=5000&transmission[]=Automatic'

