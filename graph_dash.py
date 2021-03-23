import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import random
import statistics as sts
import pandas as pd
print('Done importing!')

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

pairs = ['AUD_CAD', 'AUD_JPY', 'AUD_NZD', 'AUD_USD', 'CAD_JPY', 'DAX', 
'EUR_AUD', 'EUR_CAD', 'EUR_CHF', 'EUR_GBP', 'EUR_JPY', 'EUR_USD', 'GBP_AUD', 
'GBP_CAD', 'GBP_CHF', 'GBP_JPY', 'GBP_USD', 'NZD_USD', 'USD_CAD', 'USD_CHF', 
'USD_JPY', 'XAU_USD']

print('''
Which style of chart do you chose? 
   1. Starting points - Ending points (fixed-time)
   2. Starting points - Number of bins (fixed-time)
   3. Starting points - Now (real-time)
      ''')
style = int(input('Please enter a number: '))

if style == 1:
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

    app = dash.Dash()
    app.layout = html.Div(children=[
        dcc.Graph(id='currency_line', 
                figure={
                    'data': [
                        {'x':xs_1, 'y': ys_1, 'type':'line', 'name':'percentage'},
                        {'x':xs_1, 'y': ys_MA, 'type':'line', 'name':f'MA_{input_average}'},
                        # {'x':chosen_timemark[:input_range], 'y': chosen_blue[:input_range], 'type':'bar', 'name':'percentage'}
                        ],
                    'layout':{
                        'title': f'{result}: {custom_time} minutes'
                    }}),
        dcc.Graph(id='currency_bar', 
                figure={
                    'data': [
                        {'x':xs_1, 'y':ys_1, 'type':'bar', 'name':'percentage'}
                        ]
                    })
        ])

elif style == 2:
    result = pairs[int(input('Please select the currency code: '))]
    starting = input('Please select the starting time (eg. YYYY-MM-DD hh:mm): ')
    input_range = int(input('Please select the chart range (eg. 10bins, 20bins): '))
    custom_time = int(input('Please select the timeframe (eg. 1min, 5min): '))
    input_average = int(input('Please select the moving average period: '))

    df_custom = pd.read_csv(f'realTime_{result}.csv')
    timeframe = list(df_custom.iloc[5300:, 1].values)
    timespan = list(df_custom.iloc[5300:, 2].values)
    percentage = list(df_custom.iloc[5300:, 3].values)

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
    MA_ls = plot_MA(input_average, chosen_blue, chosen_blue_previous)

    # all data
    ys_1 = chosen_blue[:input_range]
    xs_1 = chosen_timemark[:input_range]
    ys_MA = MA_ls[:input_range]

    app = dash.Dash()
    app.layout = html.Div(children=[
        dcc.Graph(id='currency_line', 
                figure={
                    'data': [
                        {'x':xs_1, 'y': ys_1, 'type':'line', 'name':'percentage'},
                        {'x':xs_1, 'y': ys_MA, 'type':'line', 'name':f'MA_{input_average}'},
                        # {'x':chosen_timemark[:input_range], 'y': chosen_blue[:input_range], 'type':'bar', 'name':'percentage'}
                        ],
                    'layout':{
                        'title': f'{result}: {custom_time} minutes'
                    }}),
        dcc.Graph(id='currency_bar', 
                figure={
                    'data': [
                        {'x':xs_1, 'y':ys_1, 'type':'bar', 'name':'percentage'}
                        ]
                    })
        ])

elif style == 3:
    result = pairs[int(input('Please select the currency code: '))]
    starting = input('Please select the starting time (eg. YYYY-MM-DD hh:mm): ')
    input_range = int(input('Please select the chart range (eg. 10bins, 20bins): '))
    custom_time = int(input('Please select the timeframe (eg. 1min, 5min): ')) # 1min, 5min, 10min
    input_average = int(input('Please select the moving average period: '))
  
    xs_1 = deque(maxlen=input_range)
    xs_1.append(custom_time)

    app = dash.Dash(__name__)
    app.layout = html.Div(
        [
            html.Div(children=f'{result}: {custom_time} minutes'),
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(
                id='graph-update',
                interval=1000,
                n_intervals=0
            ),
        ]
    )

    @app.callback(Output('live-graph', 'figure'),
            [Input('graph-update', 'n_intervals')])

    def update_graph_line(n):
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
        MA_ls = plotMA(input_average, chosen_blue)

        # all data
        ys_1 = list(df.iloc[:, 1].values)[-input_range:]
        xs_1 = list(df.iloc[:, 0].values)[-input_range:]
        ys_MA = MA_ls[-input_range:]

        data_1 = plotly.graph_objs.Scatter(
                x=xs_1,
                y=ys_1,
                name='Percentage',
                mode= 'lines+markers'
                )
        data_2 = plotly.graph_objs.Scatter(
                x=xs_1,
                y=ys_MA,
                name=f'MA_{input_average}',
                mode= 'lines+markers',
                marker_color='rgba(152, 0, 0, .8)'
                )
        data_3 = plotly.graph_objs.Bar(
                x=xs_1,
                y=ys_1,
                name='Percentage',
                )

        return {'data': [data_1, data_2, data_3],'layout' : go.Layout(xaxis=dict(range=[min(xs_1),max(xs_1)]),
                                        

if __name__ == '__main__':
    app.run_server(debug=True)
