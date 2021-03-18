from main import scrape
import pandas as pd

'''
AUD/CAD = 0
AUD/JPY = 1
AUD/NZD = 2
AUD/USD = 3
CAD/JPY = 4
DAX = 5
EUR/AUD = 6
EUR/CAD = 7
EUR/CHF = 8
EUR/GBP = 9
EUR/JPY = 10
EUR/USD = 11
GBP/AUD = 12
GBP/CAD = 13
GBP/CHF = 14
GBP/JPY = 15
GBP/USD = 16
NZD/USD = 17
USD/CAD = 18
USD/CHF = 19
USD/JPY = 20
XAU/USD = 21
'''

i = 1
print('---Scraping EUR/AUD---')
while True:
    result = scrape(6)
    if result == None:
        continue
    elif result != None:
        try:
            print('Round: ', i)
            timemark, timespan, blue, name = result
            df = pd.DataFrame({'Time':timemark, 'Timespan':timespan, 'Data':blue})
            df.to_csv(f'realTime_{name}.csv', mode='a', header=False)
            i += 1
        except:
            continue