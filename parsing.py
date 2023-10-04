import numpy as np


def getUrls(soups):
    ads = []
    for soup in soups:
        ad = [x.find('a', class_='ad-preview__title')['href'] for x in soup.find('div', class_ = 'grid__wrapper').find_all('div', class_ = 'ad-preview')]
        ads.extend(ad)
    return ads

def getPrice(soup):
    try:
        price = soup.find('div', class_ = 'maindata').find('div', class_ = 'priceBox-price').text.strip()
    except:
        price = np.nan
    return price

def getTitle(soup):
    try:
        title = soup.find('div', class_ = 'maindata').find('h1', class_ = 'title').text.strip()
    except:
        title = np.nan
    return title

def getLocation(soup):
    try:
        location = soup.find('div', id = 'location').find('div', class_ = 'location').find('div', class_ = 'subtitle').text.strip()
    except:
        location = np.nan
    return location

def getLatLong(soup):
    try:
        lat = soup.find('div', id = 'location').find('script', type = 'text/javascript').text.strip().split(';')[0].split('=')[-1].strip()
        long = soup.find('div', id = 'location').find('script', type = 'text/javascript').text.strip().split(';')[1].split('=')[-1].strip()
    except:
        lat, long = np.nan, np.nan
    return lat, long

def getCharacteristics(soup):
    try:
        charblocks = soup.find('div', class_ = 'characteristics').find_all('div', class_ = 'charblock')
        characteristics = []
        for charblock in charblocks:
            characteristics.extend(charblock.find_all('li'))
            
        characteristics = [' '.join(x.text.split('\n')).strip() for x in characteristics]
    except:
        characteristics = np.nan
    return characteristics