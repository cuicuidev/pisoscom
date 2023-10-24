import glob
import pandas as pd
from bs4 import BeautifulSoup

from scraping.parsing import *

def run(filename):
    print('exctracting data...')

    PROVINCE = filename

    data = {
        'price' : [],
        'title' : [],
        'province' : [],
        'location' : [],
        'lat' : [],
        'lng' : [],
        'characteristics' : [],
        'agency' : [],
        'updated' : [],
        'numeric_data' : [],
    }

    files = glob.glob('html_content/*.html')

    for file in files:
        with open(file, encoding='utf-8') as f:
            source = f.read()
        soup = BeautifulSoup(source, 'html.parser')

        price = getPrice(soup)
        title = getTitle(soup)
        location = getLocation(soup)
        lat, long = getLatLong(soup)
        characteristics = getCharacteristics(soup)
        updated, agency = getAgencyDate(soup)
        numeric_data = [x for x in file[16:].split('_') if x.isnumeric()]

        data['price'].append(price)
        data['title'].append(title)
        data['province'].append(PROVINCE)
        data['location'].append(location)
        data['lat'].append(lat)
        data['lng'].append(long)
        data['characteristics'].append(characteristics)
        data['agency'].append(agency)
        data['updated'].append(updated)
        data['numeric_data'].append(numeric_data)

    df = pd.DataFrame(data)

    df.to_csv(f'data/{PROVINCE}.csv', index = False)

    print('data saved')