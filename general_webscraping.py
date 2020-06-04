#
import time
import os.path
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime


#
def date():
    #return time.strftime('%Y%m%d')
    return time.strftime("%Y%m%d%H%M%S")
   
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
            write_html(html_file, html)       
        return html

def get_soup(html):
    return BeautifulSoup(html, 'html5lib')
        
def write_html(filename, html):
    with open(filename, 'w') as f:
        f.write(html)
    return None

def remove(text, chars):
    if chars: return remove(text.replace(chars[0], ""), chars[1:])
    return text.strip()

def flatten_list(lst):
    new_lst = []
    for itm in lst:
        new_itm = flatten_item(itm)
        new_lst.append(new_itm)
    return new_lst

def flatten_item(itm):
    flatten_itm = list(itm[0])
    flatten_itm.extend(itm[1])
    return tuple(flatten_itm) 

def print_list(collection):
    for n, elem in enumerate(collection):
        print(n)
        print(elem)
        print()
    return None

def write_csv(filename, headers, vehicles):
    df = pd.DataFrame(data=vehicles, columns=headers)
    d = datetime.datetime.today()
    df['date'] = pd.Timestamp(d)
    df.to_csv(filename)
    return
