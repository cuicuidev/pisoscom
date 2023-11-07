import os
import requests
import datetime
from time import sleep

from playwright.sync_api import sync_playwright

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from CONFIG import *

base_url = 'https://www.pisos.com/'

def scrape(urls):

    try: os.mkdir('html_content/')
    except FileExistsError as e: log.error(f'util.scrape | FileExistsError | {e}')
    
    chrome_options = webdriver.ChromeOptions()
    if HEADLESS:
        log.debug(f'util.scrape | HEADLESS = {HEADLESS}')
        chrome_options.add_argument('--headless')

    log.debug(f'util.scrape | instantializing chrome')
    browser = webdriver.Chrome(options = chrome_options)
    
    for idx, url in enumerate(urls):

        browser.get(url)

        if idx == 0:

            log.debug(f'util.scrape | locating accept cookies button')
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="didomi-notice-agree-button"]'))
            )

            log.debug(f'util.scrape | clicking on accept cookies')
            element.click()

        # <SCROLLING>
        log.debug(f'util.scrape | starting to scroll')
        while True:
            log.debug(f'util.scrape | checking if at bottom')
            is_at_bottom = browser.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight")

            if is_at_bottom:
                log.debug(f'util.scrape | is_at_bottom = {is_at_bottom} | break')
                break
            
            try:
                if browser.find_element(By.XPATH, '//*[@id="location"]/script[2]'):
                    log.debug(f'util.scrape | found lat and lng script | break')
                    break
            except: pass

            log.debug(f'util.scrape | scrolling...')
            browser.execute_script("window.scroll({ top: document.body.scrollHeight, behavior: 'smooth' });")
            log.debug(f'util.scrape | calling sleep(0.2)')
            sleep(0.2)
        # </SCROLLING>
        log.debug(f'util.scrape | done scrolling')
        
        html_content = browser.page_source

        timestamp = ''.join(str(datetime.datetime.now().timestamp()).split('.'))

        soft_url = url.replace('https://www.pisos.com/comprar/', '')
        soft_url = soft_url.replace('/', '_')
        soft_url = soft_url.replace('-', '_')

        metadata = {'timestamp' : timestamp, 'soft_url' : soft_url}

        log.debug(f'util.scrape | yielding content and metadata')
        yield html_content, metadata

    log.debug(f'util.scrape | calling browser.quit()')
    browser.quit()

# def scrape(endpoints):

#     try: os.mkdir('html_content/')
#     except FileExistsError as e: log.error(f'util.scrape | FileExistsError | {e}')

#     with sync_playwright() as p:

#         log.debug(f'util.scrape | instantializing chromium')
#         b = p.chromium
#         log.debug(f'util.scrape | calling b.launch(headless = HEADLESS) | HEADLESS = {HEADLESS}')
#         browser = b.launch(headless=HEADLESS)
#         log.debug(f'util.scrape | new page')
#         page = browser.new_page()

#         for endpoint in endpoints:
#             log.info(f'util.scrape | scraping {endpoint}')
            
#             log.debug(f'util.scrape | calling page.goto(endpoint, timeout = TIMEOUT) | endpoint = {endpoint} | TIMEOUT = {TIMEOUT}')
#             page.goto(endpoint, timeout = TIMEOUT)

#             _prev_height = -1
#             _max_scrolls = 100
#             _scroll_count = 0
#             log.debug(f'util.scrape | scrolling through the page')
#             while _scroll_count < _max_scrolls:
#                 page.evaluate("window.scroll({ top: document.body.scrollHeight, behavior: 'smooth' });")
#                 page.wait_for_timeout(1000)
#                 new_height = page.evaluate("document.body.scrollHeight")
#                 if new_height == _prev_height:
#                     log.debug(f'util.scrape | stopped scrolling')
#                     break
#                 _prev_height = new_height
#                 _scroll_count += 1

#             content = page.content()

#             timestamp = ''.join(str(datetime.datetime.now().timestamp()).split('.'))

#             soft_url = endpoint.replace('https://www.pisos.com/comprar/', '')
#             soft_url = soft_url.replace('/', '_')
#             soft_url = soft_url.replace('-', '_')

#             metadata = {'timestamp' : timestamp, 'soft_url' : soft_url}

#             log.debug(f'util.scrape | yielding content and metadata')
#             yield content, metadata
                    
#         browser.close()


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
            except Exception as e:
                log.error(f'util.scanRegions | {type(e).__name__} | {e}')
        else:
            log.debug(f'util.scanRegions | n_results empty at {endpoint}')
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