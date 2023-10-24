import os
import requests
import datetime
import glob
import time
from playwright.sync_api import sync_playwright

from bs4 import BeautifulSoup



base_url = 'https://www.pisos.com/'

# def scrape(urls):
#     browser = webdriver.Chrome()
    
#     try: os.mkdir('html_content/')
#     except FileExistsError as e: print(e)
#     # finally:
#     #     raise Exception('No funcionaaaaa!!!!! :)')
    
#     for idx, url in enumerate(urls):
#         browser.get(url)
#         # browser.maximize_window()

#         if idx == 0:
#             element = WebDriverWait(browser, 10).until(
#                 EC.presence_of_element_located((By.XPATH, '//*[@id="didomi-notice-agree-button"]'))
#             )

#             element.click() # Accept cookies

#         # <SCROLLING>
#         while True:
#             is_at_bottom = browser.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight")
#             browser.execute_script("window.scroll({ top: document.body.scrollHeight, behavior: 'smooth' });")
#             if is_at_bottom:
#                 break
#             sleep(0.2)
#         # </SCROLLING>
        
#         html_content = browser.page_source

#         timestamp = ''.join(str(datetime.datetime.now().timestamp()).split('.'))

#         soft_url = url.replace('https://www.pisos.com/comprar/', '')
#         soft_url = soft_url.replace('/', '_')
#         soft_url = soft_url.replace('-', '_')

#         file_path = f'html_content/{timestamp}_{soft_url}.html'
#         try:
#             with open(file_path, 'w', encoding='utf-8') as file:
#                 file.write(html_content)
#         except Exception as e:
#             with open(file_path, 'w', encoding='utf-8') as file:
#                 file.write(repr(e))

#     browser.quit()

def scrape(endpoints):

    try: os.mkdir('html_content/')
    except FileExistsError as e: print(e)

    with sync_playwright() as p:
        b = p.chromium
        browser = b.launch(headless=True)
        page = browser.new_page()

        for endpoint in endpoints:
            page.goto(endpoint)
            print(endpoint)

            _prev_height = -1
            _max_scrolls = 100
            _scroll_count = 0
            while _scroll_count < _max_scrolls:
                page.evaluate("window.scroll({ top: document.body.scrollHeight, behavior: 'smooth' });")
                page.wait_for_timeout(1000)
                new_height = page.evaluate("document.body.scrollHeight")
                if new_height == _prev_height:
                    break
                _prev_height = new_height
                _scroll_count += 1

            content = page.content()

            timestamp = ''.join(str(datetime.datetime.now().timestamp()).split('.'))

            soft_url = endpoint.replace('https://www.pisos.com/comprar/', '')
            soft_url = soft_url.replace('/', '_')
            soft_url = soft_url.replace('-', '_')

            file_path = f'html_content/{timestamp}_{soft_url}.html'
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
            except Exception as e:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(repr(e))
                    
        browser.close()


def scanRegions(url):
    response = requests.get(url)

    print(f'URL: {url} | STATUS {response.status_code}')

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




def run(endpoint):
    print('scraping...')

    PROVINCE = endpoint

    try:
        glb = glob.glob('html_content/*.html')
        print(glb)
        size = len(glb)
        print(size)
        start = size - 1
    except: 
        start = -1

    URL = f'https://www.pisos.com/viviendas/{PROVINCE}/'


    urls = scanRegions(URL)
    urls = parseRegions(urls)
    urls = [base_url + x for x in urls]
    urls = [x.replace('//viviendas/', '/venta/pisos-') for x in urls]
    print(urls)

    if start == -1:
        print('urls loop')
        for url in urls:
            urls_ = scrapeUrls(url)
            urls_ = list(set(urls_))
            urls_ = [base_url[:-1] + x for x in urls_]
            with open('urls.csv', 'a+') as file:
                print(f'urls.csv opened at {os.getcwd()}/urls.csv')
                file.writelines([x + ',\n' for x in urls_])

    with open('urls.csv') as file:
        urls = file.read()

        urls = urls.split(',\n')

    start = time.time()
    if start != -1:
        scrape(urls[start:])
    else:
        scrape(urls[:10])
    end = time.time()
    execution_time = end - start
    print(f"Execution time: {execution_time} seconds")