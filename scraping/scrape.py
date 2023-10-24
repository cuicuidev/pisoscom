from scraping.util import *

from scraping.parsing import *
from scraping.locations import *

import numpy as np

def run(endpoint):
    print(f'SCRAPING {endpoint}')

    ############################################

    # Obtener lista de urls

    URL = f'https://www.pisos.com/viviendas/{endpoint}/'

    DATA_PATH = f'scraping/data/{endpoint}.csv'

    data_exists = bool(len(glob.glob(DATA_PATH)))

    urls_exists = bool(len(glob.glob('scraping/temp/urls.csv')))

    if data_exists and not urls_exists:
        raise Exception(f'El endpoint {endpoint} ya se descargó')

    n_rows = 0

    if not data_exists:
        with open(DATA_PATH, 'w') as f:
            f.write('price,title,province,location,lat,lng,characteristics,agency,updated,numeric_data\n')

        urls = scanRegions(URL)
        urls = parseRegions(urls)
        urls = [base_url + x for x in urls]
        urls = [x.replace('//viviendas/', '/venta/pisos-') for x in urls]

        all_urls = []
        for url in urls:
            print(url)
            urls_ = scrapeUrls(url)
            urls_ = list(set(urls_))
            urls_ = [base_url[:-1] + x for x in urls_]
            all_urls.extend([x + ',\n' for x in urls_])

        with open('scraping/temp/urls.csv', 'w') as file:
            print(f'urls.csv created at {os.getcwd()}/scraping/temp/urls.csv')
            file.writelines(all_urls)
    else:

        with open(DATA_PATH) as f:
            n_rows = len(f.read().split('\n')) - 2

    with open('scraping/temp/urls.csv') as file:
        all_urls = file.read().split(',\n')[:-1]

    # Iterar sobre urls, parsear y guardar los datos

    if n_rows != 0:
        print(f'Starting from row {n_rows}')
        to_scrape = all_urls[n_rows - 1]
    else:
        to_scrape = all_urls

    for html, metadata in scrape(to_scrape):
        with open(DATA_PATH, 'a+', encoding = 'utf-8') as f:
            soup = BeautifulSoup(html, 'html.parser')

            price = getPrice(soup)
            title = getTitle(soup)
            location = getLocation(soup)
            lat, long = getLatLong(soup)
            characteristics = getCharacteristics(soup)
            updated, agency = getAgencyDate(soup)

            data = f'{price},{title},{location},{lat},{long},{characteristics},{agency},{updated},{metadata}\n'
            f.write(data)

    ############################################
    
    print(f'{endpoint} SCRAPED SUCCESSFULLY')

    os.remove('scraper/temp/urls.csv')