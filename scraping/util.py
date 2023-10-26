import os
import requests
import datetime
import glob
import time
from playwright.sync_api import sync_playwright

from bs4 import BeautifulSoup
from CONFIG import *

base_url = 'https://www.pisos.com/'

def scrape(endpoints):

    try: os.mkdir('html_content/')
    except FileExistsError as e: log.error(f'util.scrape | FileExistsError | {e}')

    with sync_playwright() as p:

        log.debug(f'util.scrape | instantializing chromium')
        b = p.chromium
        log.debug(f'util.scrape | calling b.launch(headless = HEADLESS) | HEADLESS = {HEADLESS}')
        browser = b.launch(headless=HEADLESS)
        log.debug(f'util.scrape | new page')
        page = browser.new_page()

        for endpoint in endpoints:
            log.debug(f'util.scrape | calling page.goto(endpoint, timeout = TIMEOUT) | endpoint = {endpoint} | TIMEOUT = {TIMEOUT}')
            page.goto(endpoint, timeout = TIMEOUT)

            _prev_height = -1
            _max_scrolls = 100
            _scroll_count = 0
            log.debug(f'util.scrape | scrolling through the page')
            while _scroll_count < _max_scrolls:
                page.evaluate("window.scroll({ top: document.body.scrollHeight, behavior: 'smooth' });")
                page.wait_for_timeout(1000)
                new_height = page.evaluate("document.body.scrollHeight")
                if new_height == _prev_height:
                    log.debug(f'util.scrape | stopped scrolling')
                    break
                _prev_height = new_height
                _scroll_count += 1

            content = page.content()

            timestamp = ''.join(str(datetime.datetime.now().timestamp()).split('.'))

            soft_url = endpoint.replace('https://www.pisos.com/comprar/', '')
            soft_url = soft_url.replace('/', '_')
            soft_url = soft_url.replace('-', '_')

            metadata = {'timestamp' : timestamp, 'soft_url' : soft_url}

            log.debug(f'util.scrape | yielding content and metadata')
            yield content, metadata
                    
        browser.close()


def scanRegions(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.select('div.zoneList a.item:not(.item-subitem)')

    endpoints = {}
    for item in items:
        endpoint = item['href']
        n_results = item.find('span', class_ = 'total').text

        # <INT>
        if len(n_results) != 0:
            try:
                n_results = n_results[1:-1]
                n_results = ''.join(n_results.split('.'))
                n_results = int(n_results)
            except:
                print(f'FAIL CASTING TO INTEGER {endpoint}')
        else:
            print(f'n_results EMPTY {endpoint}')
        #</INT>

        # <RECURSSION>
        if n_results > 3000:
            endpoints[endpoint] = scanRegions(base_url[:-1] + endpoint)
        # </RECURSSION>

        else: endpoints[endpoint] = n_results

    return endpoints


def parseRegions(endpoints):

    def extract(endpoints):
        array = []
        for key, value in endpoints.items():
            if isinstance(value, int):
                array.append(key)
                continue

            data = extract(value)
            array.extend(data)

        return array
    
    endpoints = extract(endpoints)

    array = []
    
    for endpoint in endpoints:
        data = endpoint
        if '/venta/pisos-' in endpoint:
            data = endpoint.replace('/venta/pisos-', '/viviendas/')
        array.append(data)

    return array

def scrapeUrls(endpoint):
    response = requests.get(endpoint)

    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find('div', class_ = 'grid__title').find_all('span')[-1].text

    n_results = int(''.join([x for x in results if x.isnumeric()]))
    n_pages = (n_results // 30) + 1

    urls = []
    for i in range(n_pages):
        url = f'{endpoint}{i + 1}'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        ads = soup.find_all('a', class_ = 'ad-preview__title')
        urls.extend([x['href'] for x in ads])
    return urls