from pymongo import MongoClient
from random import randint
import pandas as pd
# pprint library is used to make the output look more pretty
from pprint import pprint

def PullfromMongoDB(currency_name):
    # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
    path = '/Users/admin/Environments/currencypairs/mongo_token.txt' 
    token = open(path, "r")
    client = MongoClient(token)
    database_name = 'currencypairs'
    db = client[database_name]

    # Issue the serverStatus command and print the results
    print('Check Server Status Result')
    serverStatusResult = db.command("serverStatus")
    # pprint(serverStatusResult)
    try:
        collection = db[currency_name]
    except pymongo.errors.InvalidName:
        print('Waiting for the input ...')

    mongo_data = collection.find({},{"_id":0})
    # mongo_data = collection.find({ "Time": {"$gt": "2021-04-24 11:39", '$lt':"2021-04-24 11:42"} },{"_id":0})
    # query based on condition: https://docs.mongodb.com/manual/reference/operator/query-comparison/
    # print('\nMongo data: ', mongo_data)
    mongo_docs = list(mongo_data)
    # print('\nMongo doc: ', mongo_docs)
    # print(len(mongo_docs), type(mongo_docs))
    i = 1
    custom_ls = []
    for data_point in mongo_docs:
        point = []
        for title, value in data_point.items():
            point.append(value)
            # print(f'\nItem {i}: {value}')
        # print('Point: ', point)
        custom_ls.append(point)
        i = i + 1
    # print('\nCustom ls: ', custom_ls)
    timeframe = [i[0] for i in custom_ls]
    # print('\nTimeframe: ', timeframe)
    timespan = [i[1] for i in custom_ls]
    # print('\nTimespan: ', timespan)
    percentage = [i[2] for i in custom_ls]
    # print('\nPercentage: ', percentage)
    return timeframe, timespan, percentage