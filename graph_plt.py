import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import statistics as sts
import matplotlib.gridspec as gridspec

def getDistance(base, next_point, input_time):
    distance = abs(abs((base - next_point)/60) - input_time)
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

print('All done!!!')

# Setup figure and subplots
fig = plt.figure(figsize = (20, 5))

gs1 = gridspec.GridSpec(2, 1)
ax = fig.add_subplot(gs1[0])
ax2 = fig.add_subplot(gs1[1])

# Turn on grids
ax.grid(True)

# set label names
ax.set_xlabel("Timeframe")
ax.set_ylabel("Percentage")


pairs = ['AUD_CAD', 'AUD_JPY', 'AUD_NZD', 'AUD_USD', 'CAD_JPY', 'DAX', 
'EUR_AUD', 'EUR_CAD', 'EUR_CHF', 'EUR_GBP', 'EUR_JPY', 'EUR_USD', 'GBP_AUD', 
'GBP_CAD', 'GBP_CHF', 'GBP_JPY', 'GBP_USD', 'NZD_USD', 'USD_CAD', 'USD_CHF', 
'USD_JPY', 'XAU_USD']

print('''
Which style of chart do you chose? 
   1. The latest X bins (real-time)
   2. Starting points - Now (real-time)
   3. Starting points - Ending points (fixed-time)
   4. Starting points - Number of bins (fixed-time)
      ''')
style = int(input('Please enter a number: '))

if style == 1:
    input_range = int(input('Please select the chart range (eg. 10bins, 20bins): '))
    custom_time = int(input('Please select the timeframe (eg. 1min, 5min): ')) # 1min, 5min, 10min
    result = pairs[int(input('Please select the currency code: '))]
    input_average = int(input('Please select the moving average period: '))

    def animate(i):
        df_custom = pd.read_csv(f'realTime_{result}.csv')
        timeframe = list(df_custom.iloc[:, 1].values)
        timespan = list(df_custom.iloc[:, 2].values)
        percentage = list(df_custom.iloc[:, 3].values)

        all_blue = []
        for i in range(len(timeframe)):
            all_blue.append([timeframe[i], timespan[i], percentage[i]])

        custom = getChosenPoints(custom_time, all_blue)

        chosen_timemark = [i[0] for i in custom]
        chosen_blue = [i[-1] for i in custom]
        df = pd.DataFrame({'Time':chosen_timemark,'Data':chosen_blue})

        # all data
        ys_1 = list(df.iloc[:, 1].values)[-input_range:]
        xs_1 = list(df.iloc[:, 0].values)[-input_range:]
        MA_ls = plotMA(input_average, chosen_blue)
        ys_MA = MA_ls[-input_range:]

        ax.clear()
        ax2.clear()
        line1, = ax.plot(xs_1, ys_1, label="Percentage", color='blue') 
        line2, = ax.plot(xs_1, ys_MA, label="Moving Average", color='red', linestyle='dashed')
        ax.set_title(f'{result}_{custom_time}_minutes', fontsize=12)
        ax.tick_params(axis='x', labelrotation=90, labelsize=7)
        ax2.bar(x=xs_1, height=ys_1, color ='blue', width = 0.1)
        ax2.tick_params(axis='x', labelrotation=90, labelsize=7)

    ani = FuncAnimation(fig, animate, interval=1000)
    plt.tight_layout()
    plt.show()

elif style == 2:
    starting = input('Please select the starting time (eg. YYYY-MM-DD hh:mm): ')
    input_range = int(input('Please select the chart range (eg. 10bins, 20bins): '))
    custom_time = int(input('Please select the timeframe (eg. 1min, 5min): ')) # 1min, 5min, 10min
    result = pairs[int(input('Please select the currency code: '))]
    input_average = int(input('Please select the moving average period: '))
    
    def animate(i):
        df_custom = pd.read_csv(f'realTime_{result}.csv')
        timeframe = list(df_custom.iloc[:, 1].values)
        timespan = list(df_custom.iloc[:, 2].values)
        percentage = list(df_custom.iloc[:, 3].values)

        for a in timeframe:
            if starting in a:
                index = timeframe.index(a)
        
        starting_point = index
                
        all_blue = []
        for b in range(len(timeframe)):
            if b >= starting_point:
                all_blue.append([timeframe[b], timespan[b], percentage[b]])

        custom = getChosenPoints(custom_time, all_blue)

        chosen_timemark = [i[0] for i in custom]
        chosen_blue = [i[-1] for i in custom]
        df = pd.DataFrame({'Time':chosen_timemark,'Data':chosen_blue})

        # all data
        ys_1 = list(df.iloc[:, 1].values)[-input_range:]
        xs_1 = list(df.iloc[:, 0].values)[-input_range:]
        MA_ls = plotMA(input_average, chosen_blue)
        ys_MA = MA_ls[-input_range:]

        ax.clear()
        ax2.clear()
        line1, = ax.plot(xs_1, ys_1, label="Percentage", color='blue') 
        line2, = ax.plot(xs_1, ys_MA, label="Moving Average", color='red', linestyle='dashed')
        ax.set_title(f'{result}_{custom_time}_minutes', fontsize=12)
        ax.tick_params(axis='x', labelrotation=90, labelsize=7)
        ax2.bar(x=xs_1, height=ys_1, color ='blue', width = 0.1)
        ax2.tick_params(axis='x', labelrotation=90, labelsize=7)

    ani = FuncAnimation(fig, animate, interval=1000)
    plt.tight_layout()
    plt.show()

elif style == 3:
    starting = input('Please select the starting time (eg. YYYY-MM-DD hh:mm): ')
    ending = input('Please select the ending time (eg. YYYY-MM-DD hh:mm): ')
    custom_time = int(input('Please select the timeframe (eg. 1min, 5min): '))
    result = pairs[int(input('Please select the currency code: '))]
    input_average = int(input('Please select the moving average period: '))

    df_custom = pd.read_csv(f'realTime_{result}.csv')
    timeframe = list(df_custom.iloc[:, 1].values)
    timespan = list(df_custom.iloc[:, 2].values)
    percentage = list(df_custom.iloc[:, 3].values)

    for a in timeframe:
        if starting in a:
            index_start = timeframe.index(a)
            break
    starting_point = index_start

    for a_ in timeframe:      
        if ending in a_:
            index_end = timeframe.index(a_)
            break
    ending_point = index_end
            
    all_blue = []
    for b in range(len(timeframe)):
        if index_start <= b <= index_end:
            all_blue.append([timeframe[b], timespan[b], percentage[b]])
    
    # We need to find all the blue data first
    all_blue_all = []
    for c in range(len(timeframe)):
        all_blue_all.append([timeframe[c], timespan[c], percentage[c]])

    all_blue_previous = []
    for i in all_blue_all[:index_end]:
        if i not in all_blue:
            all_blue_previous.append(i) 
    all_blue_previous.append(all_blue_all[index_start]) # We need to append the starting point of the chosen data in the end, since it will become the base when we pass this list to our function getPreviousPoint()
    
    custom = getChosenPoints(custom_time, all_blue)

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

    line1, = ax.plot(xs_1, ys_1, label="Percentage", color='blue') 
    line2, = ax.plot(xs_1, ys_MA, label="Moving Average", color='red', linestyle='dashed')

    ax.set_title(f'{custom_time}_minutes', fontsize=12)
    ax.tick_params(axis='x', labelrotation=90, labelsize=7)
    ax2.bar(x=xs_1, height=ys_1, color ='blue', width = 0.1)
    ax2.tick_params(axis='x', labelrotation=90, labelsize=7)

    plt.show()

elif style == 4:
    starting = input('Please select the starting time (eg. YYYY-MM-DD hh:mm): ')
    input_range = int(input('Please select the chart range (eg. 10bins, 20bins): '))
    custom_time = int(input('Please select the timeframe (eg. 1min, 5min): '))
    result = pairs[int(input('Please select the currency code: '))]
    input_average = int(input('Please select the moving average period: '))

    df_custom = pd.read_csv(f'realTime_{result}.csv')
    timeframe = list(df_custom.iloc[:, 1].values)
    timespan = list(df_custom.iloc[:, 2].values)
    percentage = list(df_custom.iloc[:, 3].values)

    for a in timeframe:
        if starting in a:
            index_start = timeframe.index(a)
            break
    starting_point = index_start
            
    all_blue = []
    for b in range(len(timeframe)):
        if index_start <= b:
            all_blue.append([timeframe[b], timespan[b], percentage[b]])
    
    # We need to find all the blue data first
    all_blue_all = []
    for c in range(len(timeframe)):
        all_blue_all.append([timeframe[c], timespan[c], percentage[c]])

    all_blue_previous = []
    for i in all_blue_all:
        if i not in all_blue:
            all_blue_previous.append(i) 
    all_blue_previous.append(all_blue_all[index_start]) # We need to append the starting point of the chosen data in the end, since it will become the base when we pass this list to our function getPreviousPoint()
    
    custom = getChosenPoints(custom_time, all_blue)

    custom_previous = getChosenPoints(custom_time, all_blue_previous[::-1])
    custom_previous_chosen = custom_previous[1:input_average]
    custom_previous_chosen_reverse = custom_previous_chosen[::-1]

    chosen_timemark = [i[0] for i in custom]
    chosen_blue = [i[-1] for i in custom]
    chosen_timemark_previous  = [i[0] for i in custom_previous_chosen_reverse]
    chosen_blue_previous = [i[-1] for i in custom_previous_chosen_reverse]

    # all data
    ys_1 = chosen_blue[:input_range]
    xs_1 = chosen_timemark[:input_range]
    MA_ls = plot_MA(input_average, chosen_blue, chosen_blue_previous)
    ys_MA = MA_ls[:input_range]

    line1, = ax.plot(xs_1, ys_1, label="Percentage", color='blue') 
    line2, = ax.plot(xs_1, ys_MA, label="Moving Average", color='red', linestyle='dashed')

    ax.set_title(f'{custom_time}_minutes', fontsize=12)
    ax.tick_params(axis='x', labelrotation=90, labelsize=7)
    ax2.bar(x=xs_1, height=ys_1, color ='blue', width = 0.1)
    ax2.tick_params(axis='x', labelrotation=90, labelsize=7)

    plt.show()


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