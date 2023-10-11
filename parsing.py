import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import ast
import requests

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
    try:
        owner_data = soup.find('div', class_ = 'owner-data')
        updated_date_text = owner_data.find('div', class_ = 'updated-date').text.strip()

        agency_text = ' '.join([x for x in owner_data.text.strip().split() if x not in updated_date_text])

        updated_date = ''.join([x for x in updated_date_text if x.isnumeric()])
        date = datetime.datetime.strptime(updated_date, '%d%M%Y')
        timestamp = date.timestamp()
    except:
        agency_text = np.nan
        timestamp = np.nan

    return timestamp, agency_text

##############################################################################################################

def tryInt(n):
    try:
        return int(''.join(n[:-2].split('.')))
    except: return np.nan
    
def tryLiteralEval(row):
    try:
        return ast.literal_eval(row)
    except:
        return lambda _: np.nan

##############################################################################################################

# HAY QUE REFACTORIZAR ESTE CHURRO HORRIBLE!!!!!!!

def freeChurro(df):
    columns = []
    characteristics = df['characteristics'].iloc

    for chars in characteristics:
        for char in chars:
            vals = char.split(':')
            if isinstance(vals, list):
                columns.append(vals[0])
            else:
                columns.append(vals)

    columns = [x.strip() for x in columns]
    columns = list(set(columns))
    data = []

    for chars in characteristics:

        dict_data = {}

        for char in chars:
            content = char.split(':')
            if len(content) == 2:
                key, value = content
                key = key.strip()
                dict_data[key] = value
            else:
                key, value = content[0], content[0]
                key = key.strip()
                dict_data[key] = value

        dict_columns = {}

        for column in columns:
            for key, value in dict_data.items():
                if key == column:
                    dict_columns[column] = value
            
        for column in columns:
            if dict_columns.get(column) is None:
                dict_columns[column] = np.nan

        data.append(dict_columns)
        
    return pd.DataFrame(data)

# HAY QUE REFACTORIZAR ESTE CHURRO HORRIBLE!!!!!!!

##############################################################################################################

def nanPercentage(col):
    orig_size = len(col)
    drop_size = len(col.dropna())
    return 1 - drop_size/orig_size

def nanReport(threshold, df_):
    df = df_[[col for col in df_.columns if nanPercentage(df_[col]) < threshold]]
    print(f'Porcentaje de valores perdidos en total: {1- df.dropna().shape[0] / df.shape[0]}')
    print(f'Columnas conservadas: {len(df.columns)}')
    return df

##############################################################################################################

def getType(df):
    type_ = []
    
    for n in df['title']:
        if pd.isna(n):
            type_.append(np.nan)
            continue
        if len(n) != 1:
            name = n.split()[0]
            type_.append(name)
        else: type_.append(n)
    
    df['type'] = type_
    
    return df

def getStreetType(df):
    
    types = ['calle', 'c', 'avenida', 'avda', 'av', 'plaza', 'pz', 'carretera', 'bulevar', 'boulevard', 'parque', 'paseo', 'autovía', 'autovia']
    patterns = [f'[ ]*{x}[ .] ' for x in types]
    
    street = []
    
    for n in df['location']:
        if pd.isna(n):
            street.append(np.nan)
            continue
        
        matches = []
        
        for pattern in patterns:
            match_ = re.match(pattern, n.lower())
            if match_ is not None:
                matches.append(match_)
            else: matches.append(False)
        
        if any(matches):
            street.append(' '.join([x for x in matches if x]))
        else: street.append(np.nan)
    
    df['street'] = street
    
    return df

# def getStreet(df):
#     street = []
    
#     for n in df['location']:
#         if pd.isna(n):
#             street.append(np.nan)
#             continue
#         if len(n) != 1:
#             name = n.split()[0]
#             street.append(name)
#         else: street.append(n)
    
#     df['street'] = street
    
#     return df