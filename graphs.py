import statistics as sts
import pandas as pd
from pymongo import MongoClient
print('Done importing!')

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb+srv://narian:kingboss007@cluster0.kxhan.mongodb.net/currencypairs?retryWrites=true&w=majority")
database_name = 'currencypairs'
db = client[database_name]
print(f'Connected to MongoDB: {database_name}')

# Issue the serverStatus command and print the results
print('Check Server Status Result')
serverStatusResult = db.command("serverStatus")
# pprint(serverStatusResult)

def getDistance(base, next_point, input_time):
    distance = abs(abs((int(base) - int(next_point))/60) - int(input_time))
    return distance

def getNextChosenPoint(input_time, ls, start_point_index):
    comparison_group = []

    for i in ls[start_point_index+1:]:
        base = ls[start_point_index][1]
        next_point = i[1]
        distance_base_nextpoint = getDistance(base, next_point, input_time)
        if -input_time <= distance_base_nextpoint <= input_time:
            comparison_group.append([distance_base_nextpoint, i])
        else:
            break

    if len(comparison_group) > 0:
        chosen_distance = min(comparison_group)
        next_chosen_point = chosen_distance[1]
        next_chosen_point_index = ls.index(next_chosen_point)

    elif len(comparison_group) == 0:
        try:
            next_chosen_point = ls[start_point_index + 1]
            next_chosen_point_index = ls.index(next_chosen_point)
            
        except IndexError:
            return

    return next_chosen_point_index

def getChosenPoints(input_time, ls):
    start_point_number = 0
    chosen_points = [ls[start_point_number]]
    while start_point_number < len(ls):
        next_chosen_point = getNextChosenPoint(input_time, ls, start_point_number)
        try:
            chosen_points.append(ls[next_chosen_point])
            start_point_number = next_chosen_point
        except TypeError:
            break
    
    return chosen_points

def plotMA(input_average, ls):
    MA_ls = []
    for n in range(len(ls)):
        if n >= (input_average-1):
            data_range = ls[n-(input_average-1):n+1]
            MA = sts.mean(data_range)
        else:
            MA = 0
        MA_ls.append(MA)
    return MA_ls

def plot_MA(input_average, custom, custom_previous_chosen_reverse):
    MA_ls = []
    MA_custom = custom_previous_chosen_reverse + custom
    for n in range(len(custom)):
        data_range = MA_custom[n:input_average+n]
        MA = sts.mean(data_range)
        MA_ls.append(MA)
    return MA_ls

starting_point = 0
ending_point = -1
xs_1 = []
ys_1 = []
ys_MA = []

def plotChart(pair_input, style_input, starting, ending, input_range, custom_time, input_average, starting_point, ending_point, xs_1, ys_1, ys_MA, timeframe, timespan, percentage):
    if style_input == 1:
        print('Initializing style 1 ...')   

        # Processing data
        for a in timeframe:
            if starting in a:
                starting_point = timeframe.index(a)
                break

        for a_ in timeframe:      
            if ending in a_:
                ending_point = timeframe.index(a_)
                break  

        # filter the data points in the chosen timeframe
        all_chosen_blue = []
        for b in range(len(timeframe)):
            try:
                if starting_point <= b <= ending_point:
                    all_chosen_blue.append([timeframe[b], timespan[b], percentage[b]])
            except:
                print('Waiting to proceed ...')
        
        # We need to find all the blue data first
        all_blue_all = []
        for c in range(len(timeframe)):
            all_blue_all.append([timeframe[c], timespan[c], percentage[c]])

        # We need to find data points before the chosen timeframe to calculate the Moving Average
        all_blue_previous = []
        for i in all_blue_all[:starting_point+1]: # loop through the part of the DB that are before the chosen timeframe
            if i not in all_chosen_blue:
                all_blue_previous.append(i) 
        try:
            all_blue_previous.append(all_blue_all[starting_point])
        except UnboundLocalError:
            print('OMG ...')

        custom = getChosenPoints(custom_time, all_chosen_blue)

        custom_previous = getChosenPoints(custom_time, all_blue_previous[::-1])
        custom_previous_chosen = custom_previous[1:input_average]
        custom_previous_chosen_reverse = custom_previous_chosen[::-1]

        chosen_timemark = [i[0] for i in custom]
        chosen_blue = [i[-1] for i in custom]
        chosen_timemark_previous  = [i[0] for i in custom_previous_chosen_reverse]
        chosen_blue_previous = [i[-1] for i in custom_previous_chosen_reverse]

        # all data
        ys_1 = chosen_blue
        xs_1 = chosen_timemark
        MA_ls = plot_MA(input_average, chosen_blue, chosen_blue_previous)
        ys_MA = MA_ls

    elif style_input == 2:
        print('Initializing style 2 ...')

        # Processing data
        for a in timeframe:
            if starting in a:
                starting_point = timeframe.index(a)
                break
                    
        all_chosen_blue = []
        for b in range(len(timeframe)):
            if starting_point <= b:
                all_chosen_blue.append([timeframe[b], timespan[b], percentage[b]])

        # We need to find all the blue data first
        all_blue_all = []
        for c in range(len(timeframe)):
            all_blue_all.append([timeframe[c], timespan[c], percentage[c]])

        all_blue_previous = []
        for i in all_blue_all:
            if i not in all_chosen_blue:
                all_blue_previous.append(i) 
        all_blue_previous.append(all_blue_all[starting_point]) # We need to append the starting point of the chosen data in the end, since it will become the base when we pass this list to our function getPreviousPoint()


        custom = getChosenPoints(custom_time, all_chosen_blue)

        custom_previous = getChosenPoints(custom_time, all_blue_previous[::-1])
        custom_previous_chosen = custom_previous[1:input_average]
        custom_previous_chosen_reverse = custom_previous_chosen[::-1]

        chosen_timemark = [i[0] for i in custom]
        chosen_blue = [i[-1] for i in custom]
        chosen_timemark_previous  = [i[0] for i in custom_previous_chosen_reverse]
        chosen_blue_previous = [i[-1] for i in custom_previous_chosen_reverse]
        MA_ls = plot_MA(input_average, chosen_blue, chosen_blue_previous)

        # all data
        ys_1 = chosen_blue[:input_range]
        xs_1 = chosen_timemark[:input_range]
        ys_MA = MA_ls[:input_range]

    return xs_1, ys_1, ys_MA
