#
import csv
import general_webscraping as gws


#
INPUT_FILENAME = "./input/make-model_urls.txt"


#
def soup_find_ret_text(soup, find_name, find_attrs=None, ret_attr_text=None):
    result = soup.find(find_name, find_attrs)
    if result is not None:
        if ret_attr_text is not None:
            result = result.find(ret_attr_text)
            if result is not None:
                result = result.text
        else:
            result = result.text
    return result

def get_urls(filename=INPUT_FILENAME):
    with open(filename, "r", newline="", encoding="ascii") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar="\"", escapechar="")
        rows = list(reader)   
    return rows

def get_html_filename(date, make_model, page):
    return "./html/"+ date + "_" + make_model + "_page" +str(page) + ".html"
 
def get_csv_filename(date, make_model):
    return "./output/" + date + "_" + make_model + ".csv" 

def get_listings_headers():
    return ['year_make_model_1', 'detail_url']

def extract_listings(html, limit_= None):
    soup = gws.get_soup(html)   #BeautifulSoup(html, 'html5lib')
    # next_page_url; if this exists then over 30 vehicles and use below
    next_page_url = soup.find('a', {'data-test':'Pagination-directional-next'})
    if next_page_url is not None:
        next_page_url = "https://penfed.truecar.com" + next_page_url['href']
        
    listings = []
    vehicle_listings = soup.find_all('a', {'data-test':'usedListing'}, limit=limit_)
    if vehicle_listings is not []:
        for vehicle_listing in vehicle_listings:
            
            year = soup_find_ret_text(vehicle_listing, 'span', {'class':'vehicle-card-year'})
            make_model = soup_find_ret_text(vehicle_listing, 'span', {'class':'vehicle-header-make-model'})
            
            if year is not None and make_model is not None:
                title_ = year + ' ' + make_model
            else:
                title_ = None
            
            href = vehicle_listing['href']
            if href is not None:
                detail_url = "https://penfed.truecar.com" + href
            else:
                detail_url = None
            
            t = tuple([title_, detail_url])
            listings.append(t)
    else:
        vehicle_listings = soup.find_all('a', {'data-test': 'vehicleListingCard'}, limit=limit_)
        for vehicle_listing in vehicle_listings:
            title_ = vehicle_listing.h4
            if title_ is not None:
                title_ = title_.text
            
            href = vehicle_listing['href']
            if href is not None:
                detail_url = "https://penfed.truecar.com" + href
            else:
                detail_url = None
            
            t = tuple([title_, detail_url])
            listings.append(t)
    return next_page_url, listings

def get_vehicle_details_headers():
    return ['vin', 'price_rating', 'vehicle_price', 'year_make_model_2', 'trim', 'location', 'mileage', 'exterior_color', 'interior_color',
            'mpg', 'engine', 'transmission', 'drive_type', 'fuel_type', 'accident_check', 'usage', 'title', 
            'number_of_owners']

def extract_vehicle_details(vehicles):
    details = []
    for vehicle in vehicles:
        detail_url = vehicle[1]
        detail_html = gws.get_html(detail_url)
        
        if not detail_html:
            return None
        
        soup = gws.get_soup(detail_html) #BeautifulSoup(detail_html, 'html5lib')
        detail = extract_detail(soup)
        details.append(detail)

    return details

def extract_detail(soup):
    #
    def transform_vin(vin):
        if vin is not None:
            vin = gws.remove(vin, ['VIN:'])
        return vin
    
    def transform_vehicle_price(vehicle_price):
        if vehicle_price is not None:
            vehicle_price = gws.remove(vehicle_price, '$,')
            vehicle_price = int(vehicle_price)
        return vehicle_price
    
    def transform_mileage(mileage):
        if mileage is not None:
            mileage = gws.remove(mileage, ['Miles',','])
            mileage = int(mileage)
        return mileage
    
    def transform_accident_check(accident_check):
        if accident_check is not None:
            accident_check = gws.remove(accident_check.text, ['reported', 'accidents'])
            accident_check = int(accident_check)    
        return accident_check
    
    def transform_number_of_owners(number_of_owners):
        return int(number_of_owners)

    def extract_accident_check_and_usage(condition_history_values_lis):
        accident_check = transform_accident_check(condition_history_values_lis[0])
        
        usage = condition_history_values_lis[1]
        if usage is not None:
            usage = usage.text
            
        return accident_check, usage
        
    def extract_title_and_number_of_owners(condition_history_values_lis):
        title = condition_history_values_lis[0]
        if title is not None:
            title = title.text
       
        number_of_owners = condition_history_values_lis[1]
        if number_of_owners is not None:
            number_of_owners = transform_number_of_owners(number_of_owners.text)  
        
        return title, number_of_owners
    
    def extract_accident_check_usage_title_number_of_owners(soup):
        condition_history = soup.find('div', {'data-qa':'ConditionHistory'})
        condition_history_cols = condition_history.find_all('div', {'data-qa':'Col'})
    
        condition_history_values = condition_history_cols[0]
        condition_history_values_lis = condition_history_values.find_all('li')
        accident_check, usage = extract_accident_check_and_usage(condition_history_values_lis)
    
        condition_history_values = condition_history_cols[1]
        condition_history_values_lis = condition_history_values.find_all('li')
        title, number_of_owners = extract_title_and_number_of_owners(condition_history_values_lis)
        
        return accident_check, usage, title, number_of_owners

    # extract fields
    vin = transform_vin(soup_find_ret_text(soup, 'li', {'data-qa':'vin-number'}))
    
    price_rating = soup_find_ret_text(soup, 'span', {'class':'graph-icon-title'})
        
    vehicle_price = transform_vehicle_price(soup_find_ret_text(soup, 'strong', {'data-test':'vehiclePrice'}))    

    year_make_model = soup_find_ret_text(soup, 'div', {'class':'heading-3'})
    
    trim_ = soup_find_ret_text(soup, 'div', {'class':'heading-4'})
    
    location = soup_find_ret_text(soup, 'span', {'data-qa':'used-vdp-header-location'})

    mileage = transform_mileage(soup_find_ret_text(soup, 'span', {'data-qa':'used-vdp-header-miles'}))

    exterior_color = soup_find_ret_text(soup, 'div', {'data-qa':'vehicle-overview-item-Exterior Color'}, 'li')

    interior_color = soup_find_ret_text(soup, 'div', {'data-qa':'vehicle-overview-item-Interior Color'}, 'li')
        
    mpg = soup_find_ret_text(soup, 'div', {'data-qa':'vehicle-overview-item-MPG'})
        
    engine = soup_find_ret_text(soup, 'div', {'data-qa':'vehicle-overview-item-Engine'}, 'li')

    transmission = soup_find_ret_text(soup, 'div', {'data-qa':'vehicle-overview-item-Transmission'}, 'li')

    drive_type = soup_find_ret_text(soup, 'div', {'data-qa':'vehicle-overview-item-Drive Type'}, 'li')

    fuel_type = soup_find_ret_text(soup, 'div', {'data-qa':'vehicle-overview-item-Fuel Type'}, 'li')

    accident_check, usage, title_, number_of_owners = extract_accident_check_usage_title_number_of_owners(soup)
    
    return tuple([vin, price_rating, vehicle_price, year_make_model, trim_, location, mileage, exterior_color, interior_color,
                  mpg, engine, transmission, drive_type, fuel_type, accident_check, usage, title_, number_of_owners])
   