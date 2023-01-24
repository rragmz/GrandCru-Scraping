import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import json
import time
from selenium.webdriver.common.by import By

URL_BASE = 'https://www.grandcru.com.ar'
XPATH_BUTTON_LOAD_MORE = '/html/body/div[4]/div[2]/div[6]/div[3]/div[2]/div[2]/a'
PAGE_WINES_WORLD = '/vinos-del-mundo'
PAGE_NATIONAL_WINES = '/vinos-argentinos'

#Fetcher
def wines_fetcher(page = ''):
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(URL_BASE + page)

    #Scrolldown the page
    for i in range(100):
        try:
            for i in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            #Click 'Load More' btn
            driver.find_element(By.XPATH, XPATH_BUTTON_LOAD_MORE).click()
            time.sleep(2)
        except:
            break

        
    page_source = driver.page_source
    driver.close()
    return page_source

def wines_parser(page):
    soup = BeautifulSoup(wines_fetcher(page), 'html.parser')
    items = soup.find_all('div', {'class':'js-item-product'})
    total_items = []
    for item in items:
        try:
            #ID
            product_id = item.find('a', {'class':'js-item-name'})['data-product-id']
            #LINK
            product_link = item.find('a')['href']
            #PHOTO
            product_image = item.find('img')['data-srcset'].split(" ",1)[0][2:]
            #NAME
            product_name = item.find('a', {'class':'js-item-name'}).text
            #PRICE
            product_price_symbol = item.find('span', {'class':'item-price'}).text.strip()
            product_price = product_price_symbol[1:].replace('.','')
            #DESCRIPTION
            script = item.find_all('script')
            script = script[0].text.strip()
            data_script = json.loads(script)
            product_description = data_script["description"].split(" -")
            #TYPE OF WINE
            type_of_wine = product_description[1].replace('Tipo de Vino: ', '')
            #COUNTRY
            country = product_description[2].replace('Pais: ', '')
            #STOCK
            raw_product_stock = item.find('span', {'class': 'hidden'})['data-store'].split("\n")
            latest_numbers_stock = [int(x.split("-")[-1]) for x in raw_product_stock]
            product_stock = ' '.join(str(x) for x in latest_numbers_stock)

            #PRODUCT_DETAILS
            product_details = {
                "product_id": product_id,
                "product-link": product_link,
                "product-image": product_image,
                "product_name": product_name,
                "product-price": product_price,
                "type-of-wine": type_of_wine,
                "country": country,
                "product-stock": product_stock
            }
            total_items.append(product_details)
        except:
            pass
    return total_items

ARGENTINE_WINES = wines_parser('/vinos-argentinos')
INTERNATIONAL_WINES = wines_parser('/vinos-del-mundo')
WINES = ARGENTINE_WINES + INTERNATIONAL_WINES
#print(WINES)