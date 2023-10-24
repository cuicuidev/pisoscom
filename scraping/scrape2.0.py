import time
from playwright.sync_api import sync_playwright

TEST =  'https://www.pisos.com/venta/pisos-gijon_concejo_xixon_conceyu_gijon/'

async_ = False

endpoints = [f'https://books.toscrape.com/catalogue/page-{i}.html' for i in range(50)]

def scrape(endpoints):
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
        browser.close()

        
        with open('example.html', 'w', encoding = 'utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    start_time = time.time()

    scrape(endpoints)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time with sync: {execution_time} seconds")



















# async def run_(endpoints):
#     async with async_playwright() as p:
#         b = p.chromium
#         browser = await b.launch(headless=True)
#         page = await browser.new_page()
        
#         for endpoint in endpoints:
#             await page.goto(endpoint)

#             _prev_height = -1
#             _max_scrolls = 100
#             _scroll_count = 0
#             while _scroll_count < _max_scrolls:
#                 # Execute JavaScript to scroll to the bottom of the page
#                 await page.evaluate("window.scroll({ top: document.body.scrollHeight, behavior: 'smooth' });")
#                 # Wait for new content to load (change this value as needed)
#                 await page.wait_for_timeout(1000)
#                 # Check whether the scroll height changed - means more pages are there
#                 new_height = await page.evaluate("document.body.scrollHeight")
#                 if new_height == _prev_height:
#                     break
#                 _prev_height = new_height
#                 _scroll_count += 1

#             content = await page.content()

            
#             with open('example.html', 'w', encoding = 'utf-8') as f:
#                 f.write(content)

        
#         await browser.close()


# async def scrape_endpoint(endpoint):
#     async with async_playwright() as p:

#         filename = endpoint[-6:]

#         b = p.chromium
#         browser = await b.launch(headless=True)
#         page = await browser.new_page()
        
#         try:
#             await page.goto(endpoint, timeout=60000)
#         except playwright.errors.TimeoutError:
#             print(f"Timeout occurred while loading {endpoint}. Skipping.")

#         _prev_height = -1
#         _max_scrolls = 100
#         _scroll_count = 0
#         while _scroll_count < _max_scrolls:
#             await page.evaluate("window.scroll({ top: document.body.scrollHeight, behavior: 'smooth' });")
#             await page.wait_for_timeout(1000)
#             new_height = await page.evaluate("document.body.scrollHeight")
#             if new_height == _prev_height:
#                 break
#             _prev_height = new_height
#             _scroll_count += 1

#         content = await page.content()
        
#         # with open(f'{filename}.html', 'w', encoding='utf-8') as f:
#         #     f.write(content)

#         await browser.close()

# async def run(endpoints):
#     tasks = [scrape_endpoint(endpoint) for endpoint in endpoints]

#     n_jobs = 5

#     for i in range(0, len(tasks), n_jobs):
#         print(i)
#         jobs = tasks[i:i+n_jobs]

#         await asyncio.gather(*jobs)

# if __name__ == '__main__':
#     start_time = time.time()

#     if async_:
#         asyncio.run(run(endpoints))
#     else:
#         asyncio.run(run_(endpoints))
#     end_time = time.time()

#     execution_time = end_time - start_time
#     print(f"Execution time with async_ = {async_}: {execution_time} seconds")

#     async_ = True

#     start_time = time.time()

#     if async_:
#         asyncio.run(run(endpoints))
#     else:
#         asyncio.run(run_(endpoints))
#     end_time = time.time()

#     execution_time = end_time - start_time
#     print(f"Execution time with async_ = {async_}: {execution_time} seconds")