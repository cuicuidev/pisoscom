import re
import numpy as np
from bs4 import BeautifulSoup
import datetime

def getUrls(soups: list[BeautifulSoup]):
    ads = []
    for soup in soups:
        ad = [x.find('a', class_='ad-preview__title')['href'] for x in soup.find('div', class_ = 'grid__wrapper').find_all('div', class_ = 'ad-preview')]
        ads.extend(ad)
    return ads

def getPrice(soup: BeautifulSoup):
    try:
        price = soup.find('div', class_ = 'maindata').find('div', class_ = 'priceBox-price').text.strip()
    except:
        price = np.nan
    return price

def getTitle(soup: BeautifulSoup):
    try:
        title = soup.find('div', class_ = 'maindata').find('h1', class_ = 'title').text.strip()
    except:
        title = np.nan
    return title

def getLocation(soup: BeautifulSoup):
    try:
        location = soup.find('div', id = 'location').find('div', class_ = 'location').find('div', class_ = 'subtitle').text.strip()
    except:
        try:
            location = soup.find('div', class_ = 'location').find('div', class_ = 'subtitle').text.strip()
        except:
            location = np.nan
    return location

def getLatLong(soup: BeautifulSoup):
    try:
        # Find all script tags with the specified type
        script_tags = soup.find_all('script', {'type': 'text/javascript'})

        # Define a regular expression pattern to match lat and long values
        pattern = re.compile(r'var _Lat = "(.*?)";\s*var _Long = "(.*?)";')

        # Iterate through script tags to find and extract lat and long values
        for script_tag in script_tags:
            match = pattern.search(script_tag.text)
            if match:
                lat, long = match.groups()
                return lat, long
        lat, long = np.nan, np.nan
    except:
        lat, long = np.nan, np.nan
    return lat, long

def getCharacteristics(soup: BeautifulSoup):
    try:
        charblocks = soup.find_all('div', class_ = 'charblock')
        characteristics = []
        for charblock in charblocks:
            characteristics.extend(charblock.find_all('li'))
        characteristics = [' '.join(x.text.split('\n')).strip() for x in characteristics]
    except:
        characteristics = np.nan
    return characteristics

def getAgencyDate(soup: BeautifulSoup):
    owner_data = soup.find('div', class_ = 'owner-data')
    updated_date_text = owner_data.find('div', class_ = 'updated-date').text.strip()

    agency_text = ' '.join([x for x in owner_data.text.strip().split() if x not in updated_date_text])

    updated_date = ''.join([x for x in updated_date_text if x.isnumeric()])
    date = datetime.datetime.strptime(updated_date, '%d%M%Y')
    timestamp = date.timestamp()

    return timestamp, agency_text