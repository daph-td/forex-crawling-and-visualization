# 1 Standard imports
import pandas as pd
import matplotlib.pyplot as plt 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime as dt
import statistics as sts
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
print('- Finish importing standard packages')

# 2 Setup selenium webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--ignore-certificate-errors')
# opt.add_experimental_option("prefs", prefs)

# 3 Initialize webdriver
driver = webdriver.Chrome('chromedriver',options=chrome_options)
print('- Finish initializing a browser')

# Page source
def initDriver(dv):
    # driver = webdriver.Chrome('chromedriver',options=opt)
    dv.get("https://www.fxblue.com/market-data/tools/sentiment")
    content = dv.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    return soup

# SentimentRow - Currencies all tags
def loadTags(soup):
    tag = soup.find('div', {'id': 'SentimentContainer'})
    all_tags = tag.find_all('div', {'class': 'SentimentRow'})
    return all_tags    

# Get the currency name and source
def getName(source):
    c_name = source.find('div', {'class': 'SentimentRowCaption'}).get_text().strip()
    return c_name

def getBlue(source):
    c_blue_str = source.find('div', {'class': 'SentimentValueCaption SentimentValueCaptionLong'}).get_text().strip()
    c_blue_fl = float(c_blue_str.replace('%', ''))
    return c_blue_fl
print('- Finish defining necessary functions')

def scrape(code):  
    blue = []
    blue_span = []
    timespan = []
    timemark = []
    page_source = initDriver(driver)
    c_tags = loadTags(page_source)
    starttime = time.time()
    now = str(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('Time start: ', now)

    if len(c_tags) == 0:
        print('Cant load the data \n')
        return None

    elif len(c_tags) != 0:
        timespan.append(starttime)
        timemark.append(now)
        try:
            blue.append(getBlue(c_tags[code]))
            blue_span.append([now, starttime, getBlue(c_tags[code])])
        except:
            pass
        print('Orginal blue: ', blue)

    print('\n')
    return timemark, timespan, blue
print('- Finish defining scraper')

pairs = ['AUD_CAD', 'AUD_JPY', 'AUD_NZD', 'AUD_USD', 'CAD_JPY', 'DAX', 
'EUR_AUD', 'EUR_CAD', 'EUR_CHF', 'EUR_GBP', 'EUR_JPY', 'EUR_USD', 'GBP_AUD', 
'GBP_CAD', 'GBP_CHF', 'GBP_JPY', 'GBP_USD', 'NZD_USD', 'USD_CAD', 'USD_CHF', 
'USD_JPY', 'XAU_USD']

i = 1

c_code = int(input('Please choose the currency based on its code: '))
name = pairs[c_code]

print(f'---Scraping {pairs[c_code]}---')
while True:
    result = scrape(c_code)
    if result == None:
        continue
    elif result != None:
        try:
            print('Round: ', i)
            timemark, timespan, blue = result
            df = pd.DataFrame({'Time':timemark, 'Timespan':timespan, 'Data':blue})
            df.to_csv(f'realTime_{name}.csv', mode='a', header=False)
            i += 1
        except:
            continue
