import requests
import re

from bs4 import BeautifulSoup

from unidecode import unidecode

def replaceWithUnderscore(names_list):
    cleaned_list = []
    for name in names_list:
        # Remove any sequence within parentheses including the parentheses
        name_no_parenthesis = re.sub(r'\(.*?\)', '', name).strip()
        # Convert to ASCII, remove tildes, and replace spaces/dashes with underscores
        cleaned_name = re.sub(r'[\s\-]+', '_', unidecode(name_no_parenthesis))
        cleaned_list.append(f"pisos-{cleaned_name}/")
    return cleaned_list


def getOffersFrom(url):
    soups = []
    for i in range(1,101):
        endpoint = f'{url}{i}/'
        response = requests.get(endpoint)
        
        if response.status_code != 200:
            return soups
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        no_results = soup.find('div', class_ = 'no-results')
        
        if no_results:
            return soups
        
        soups.append(soup.body)
        print(f'Scraped page {i}')
        #sleep(0.5)
    return soups