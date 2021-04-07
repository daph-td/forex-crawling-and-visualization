from pymongo import MongoClient
from random import randint
import pandas as pd

# pprint library is used to make the output look more pretty
from pprint import pprint

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb+srv://Kingboss01:kingboss@cluster0.arwti.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database_name = 'currencypairs'
db = client[database_name]

# Issue the serverStatus command and print the results
print('Check Server Status Result')
serverStatusResult = db.command("serverStatus")
# pprint(serverStatusResult)

#Step 2: Create sample data
pairs = ['AUD_CAD', 'AUD_JPY', 'AUD_NZD', 'AUD_USD', 'CAD_JPY', 'DAX', 
'EUR_AUD', 'EUR_CAD', 'EUR_CHF', 'EUR_GBP', 'EUR_JPY', 'EUR_USD', 'GBP_AUD', 
'GBP_CAD', 'GBP_CHF', 'GBP_JPY', 'GBP_USD', 'NZD_USD', 'USD_CAD', 'USD_CHF', 
'USD_JPY', 'XAU_USD']
currency_code = int(input('Please key in the currency code: '))
result = pairs[currency_code]
collection = db[result]

# mongo_data = collection.find({},{"_id":0})
mongo_data = collection.find({},{"_id":0})
mongo_docs = list(mongo_data)
print('\nMongo doc: ', mongo_docs)

i = 1
custom_ls = []
for data_point in mongo_docs[:50]:
    point = []
    for title, value in data_point.items():
        point.append(value)
        print(f'\nItem {i}: {value}')
    print('Point: ', point)
    custom_ls.append(point)
    i = i + 1

print('\nCustom ls: ', custom_ls)

timeframe = [i[0] for i in custom_ls]
print('\nTimeframe: ', timeframe)

timespan = [i[1] for i in custom_ls]
print('\nTimespan: ', timespan)

percentage = [i[2] for i in custom_ls]
print('\nPercentage: ', percentage)
