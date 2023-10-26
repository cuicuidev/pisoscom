from scraping.util import *

from scraping.parsing import *
from scraping.locations import *

import numpy as np

def run(endpoint):

    log.info(f'scrape.run | scraping {endpoint}')

    ############################################

    # Obtener lista de urls

    URL = f'https://www.pisos.com/viviendas/{endpoint}/'

    DATA_PATH = f'scraping/data/{endpoint}.csv'

    
    log.debug(f'scrape.run | checking if {endpoint}.csv exists at ./data/')
    data_exists = bool(len(glob.glob(DATA_PATH)))
    log.debug(f'scrape.run | data_exists = {data_exists}')

    log.debug('scrape.run | checking if urls.csv exists at ./temp/')
    urls_exists = bool(len(glob.glob('scraping/temp/urls.csv')))
    log.debug(f'scrape.run | urls_exists = {urls_exists}')

    if data_exists and not urls_exists:
        log.critical(f'scrape.run | {endpoint} has been already downloaded')
        raise Exception(f'El endpoint {endpoint} ya se descargó')

    n_rows = 0

    if not data_exists:

        log.debug(f'scrape.run | creating {endpoint}.csv at ./data/')
        with open(DATA_PATH, 'w', encoding = 'utf-8') as f:
            f.write('price,title,province,location,lat,lng,characteristics,agency,updated,numeric_data\n')
        log.debug(f'scrape.run | {endpoint}.csv created at ./data/')

        log.debug(f'scrape.run | calling scanRegions(URL) | URL = {URL}')
        urls = scanRegions(URL)
        log.debug(f'scrape.run | scanRegions() returned')

        log.debug(f'scrape.run | calling parseRegions(urls) | len(urls.keys()) = {len(urls.keys())}')
        urls = parseRegions(urls)
        log.debug(f'scrape.run | parseRegions() returned')

        log.debug(f'scrape.run | prefixing {base_url} to the urls | urls[0] = {urls[0]} | len(urls) = {len(urls)}')
        urls = [base_url + x for x in urls]
        log.debug(f'scrape.run | done prefixing')

        log.debug(f"scrape.run | replacing '//viviendas/' for '/venta/pisos-' in every url in urls | urls[0] = {urls[0]} | len(urls) = {len(urls)}")
        urls = [x.replace('//viviendas/', '/venta/pisos-') for x in urls]
        log.debug(f'scrape.run | done replacing')


        log.debug(f'scrape.run | exctracting publication urls out of pages')
        all_urls = []
        log.debug(f'scrape.run | initializing all_urls as an empty list | len(all_urls) = {len(all_urls)}')
        for url in urls:
            log.debug(f'scrape.run | calling scrapeUrls(url) | url = {url}')
            urls_ = scrapeUrls(url)
            log.debug(f'scrape.run | scrapeUrls() returned')

            log.debug(f'scrape.run | removing duplicates from urls_ | urls_[0] = {urls_[0]} | len(urls_) = {len(urls_)}')
            urls_ = list(set(urls_))
            log.debug(f'scrape.run | done removing duplicates')

            log.debug(f'scrape.run | prefixing {base_url[:-1]} to each url in urls_ | urls_[0] = {urls_[0]} | len(urls_) = {len(urls_)}')
            urls_ = [base_url[:-1] + x for x in urls_]
            log.debug(f'scrape.run | done prefixing')

            log.debug(f'scrape.run | extending all_urls with urls_ | urls_[0] = {urls_[0]} | len(urls_) = {len(urls_)}')
            all_urls.extend([x + ',\n' for x in urls_])
            log.debug(f'scrape.run | done extending all_urls')

        log.debug(f'scrape.run | creating urls.csv at ./temp/')
        with open('scraping/temp/urls.csv', 'w') as file:
            file.writelines(all_urls)
        log.debug(f'scrape.run | urls.csv created at ./temp/')

    else:

        log.debug(f'scrape.run | reading {endpoint}.csv at ./data/')
        with open(DATA_PATH, encoding = 'utf-8') as f:
            log.debug(f'scrape.run | calculating n_rows')
            n_rows = len(f.read().split('\n')) - 2
            log.debug(f'scrape.run | n_rows = {n_rows}')
        log.debug(f'scrape.run | done reading')

    log.debug(f'scrape.run | reading urls.csv at ./temp/')
    with open('scraping/temp/urls.csv') as file:
        log.debug(f'scrape.run | getting all_urls from urls.csv')
        all_urls = file.read().split(',\n')[:-1]
    log.debug(f'scrape.run | done reading')

    # Iterar sobre urls, parsear y guardar los datos

    if n_rows != 0:
        log.debug(f'scrape.run | slicing all_urls at [{n_rows -1}:]')
        to_scrape = all_urls[n_rows - 1:]
    else:
        to_scrape = all_urls

    try:
        log.debug(f'scrape.run | looping through scrape(to_scrape) | to_scrape[0] = {to_scrape[0]} | len(to_scrape) = {len(to_scrape)}')
        for html, metadata in scrape(to_scrape):

            log.debug(f'scrape.run | instantializing BeautifulSoup object')
            soup = BeautifulSoup(html, 'html.parser')

            log.debug(f'scrape.run | calling getPrice(soup)')
            price = getPrice(soup)
            log.debug(f'scrape.run | getPrice() returned')

            log.debug(f'scrape.run | calling getTitle(soup)')
            title = getTitle(soup)
            log.debug(f'scrape.run | getTitle(soup) returned')

            log.debug(f'scrape.run | calling getLocation(soup)')
            location = getLocation(soup)
            log.debug(f'scrape.run | getLocation(soup) returned')

            log.debug(f'scrape.run | calling getLatLong(soup)')
            lat, long = getLatLong(soup)
            log.debug(f'scrape.run | getLatLong(soup) returned')

            log.debug(f'scrape.run | calling getCharacteristics(soup)')
            characteristics = getCharacteristics(soup)
            log.debug(f'scrape.run | getCharacteristics(soup) returned')

            log.debug(f'scrape.run | calling getAgencyDate(soup)')
            updated, agency = getAgencyDate(soup)
            log.debug(f'scrape.run | getAgencyDate(soup) returned')

            data = f'{price},{title},{location},{lat},{long},{characteristics},{agency},{updated},{metadata}'

            log.debug(f'scrape.run | appending to {endpoint}.csv at ./data/')
            with open(DATA_PATH, 'a+', encoding = 'utf-8') as f:
                log.debug(f'scrape.run | appending data')
                f.write(data)

                log.debug(f'scrape.run | appending a line break')
                f.write('\n')
            log.debug(f'scrape.run | done appending')

    except KeyboardInterrupt as e:
        log.error(f'scrape.run | KeyboardInterrupt | {e}')
        log.error(f'scrape.run | return None')
        return

    except Exception as e:
        log.error(f'scrape.run | {type(e).__name__} | {e}') 
        log.error(f'scrape.run | loop failed, starting recursively...')
        run(endpoint)
        log.debug(f'scrape.run | return None')
        return

    ############################################
    
    log.info(f'scrape.run | {endpoint} scraped successfully')

    log.debug(f'scrape.run | cleaning files at ./temp/')
    os.remove('scraper/temp/urls.csv')
    log.debug(f'scrape.run | return None')