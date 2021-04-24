import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import statistics as sts
import pandas as pd
from mongo_data import *
from graph_dash import *
print('Done importing!')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
graph_test = dash.Dash(__name__, external_stylesheets=external_stylesheets)

graph_test.layout = html.Div(children=[

    html.Div([
        html.Div([
            html.B('Please select one of the following currency pairs: '),
            html.Div('AUD_USD, EUR_JPY, EUR_USD, GBP_USD'),
            dcc.Input(id='pair_input', type='text', value='', placeholder='Enter a pair ...', debounce=True),
            # html.Div(id='pair_output'),
        ]),

        html.Div([
            html.B('Please select a style of chart: '),
            html.Div('Style 1. Starting points - Ending points (fixed-time)'),
            html.Div('Style 2. Starting points - Number of bins (fixed-time)'),
            dcc.Input(id='style_input', type='number', value='', placeholder='Enter a number ...', debounce=True),
        ], style={"margin-top": "20px"}),

        html.Div([
            html.B('Please select the starting time'),
            html.Div('(eg. YYYY-MM-DD hh:mm)'),
            dcc.Input(id='starting', type='text', value='', placeholder='Enter a value ...', debounce=True),
            # html.Div(id='starting_output'),
        ], style={"margin-top": "20px"}),

        html.Div([
            html.B('Please select the ending time'),
            html.Div('(eg. YYYY-MM-DD hh:mm)'),
            dcc.Input(id='ending', type='text', value='', placeholder='Enter a value ...', debounce=True),
            # html.Div(id='ending_output'),
        ], style={"margin-top": "20px"}),

        html.Div([
            html.B('Please select the chart range'),
            html.Div('(eg. 10bins, 20bins)'),
            dcc.Input(id='input_range', type='number', value='', placeholder='Enter a value ...', debounce=True),
            # html.Div(id='input_range_output'),
        ], style={"margin-top": "20px"}),

        html.Div([
            html.B('Please select the timeframe'),
            html.Div('(eg. 1min, 5min, 1440min)'),
            dcc.Input(id='custom_time', type='number', value='', placeholder='Enter a value ...', debounce=True),
            # html.Div(id='custom_time_output'),
        ], style={"margin-top": "20px"}),

        html.Div([
            html.B('Please select the moving average period'),
            html.Br(),
            dcc.Input(id='input_average', type='number', value='', placeholder='Enter a value ...', debounce=True),
            # html.Div(id='input_average_output'),
        ], style={"margin-top": "20px"})

     ], style={'columnCount': 2}),

    html.Div(id='style_output')
])

@graph_test.callback(
    Output(component_id="style_output", component_property="children"),
    Input(component_id="pair_input", component_property="value"),    
    Input(component_id="style_input", component_property="value"),
    Input(component_id="starting", component_property="value"),
    Input(component_id="ending", component_property="value"),
    Input(component_id="input_range", component_property="value"),
    Input(component_id="custom_time", component_property="value"),
    Input(component_id="input_average", component_property="value")
)

def update_data(pair_input, style_input, starting, ending, input_range, custom_time, input_average):
    xs_1 = []
    ys_1 = []
    ys_MA = []
    ending_point = -1
    starting_point = 0
    timeframe, timespan, percentage = PullfromMongoDB(pair_input)
    xs_1, ys_1, ys_MA = plotChart(pair_input, style_input, starting, ending, input_range, custom_time, input_average, starting_point, ending_point, xs_1, ys_1, ys_MA, timeframe, timespan, percentage)

    # if style_input == 1:
    #     print('Initializing style 1 ...')   

    #     # Processing data
    #     for a in timeframe:
    #         if starting in a:
    #             starting_point = timeframe.index(a)
    #             break

    #     for a_ in timeframe:      
    #         if ending in a_:
    #             ending_point = timeframe.index(a_)
    #             break  

    #     # filter the data points in the chosen timeframe
    #     all_chosen_blue = []
    #     for b in range(len(timeframe)):
    #         try:
    #             if starting_point <= b <= ending_point:
    #                 all_chosen_blue.append([timeframe[b], timespan[b], percentage[b]])
    #         except:
    #             print('Waiting to proceed ...')
        
    #     # We need to find all the blue data first
    #     all_blue_all = []
    #     for c in range(len(timeframe)):
    #         all_blue_all.append([timeframe[c], timespan[c], percentage[c]])

    #     # We need to find data points before the chosen timeframe to calculate the Moving Average
    #     all_blue_previous = []
    #     for i in all_blue_all[:starting_point+1]: # loop through the part of the DB that are before the chosen timeframe
    #         if i not in all_chosen_blue:
    #             all_blue_previous.append(i) 
    #     try:
    #         all_blue_previous.append(all_blue_all[starting_point])
    #     except UnboundLocalError:
    #         print('OMG ...')

    #     custom = getChosenPoints(custom_time, all_chosen_blue)

    #     custom_previous = getChosenPoints(custom_time, all_blue_previous[::-1])
    #     custom_previous_chosen = custom_previous[1:input_average]
    #     custom_previous_chosen_reverse = custom_previous_chosen[::-1]

    #     chosen_timemark = [i[0] for i in custom]
    #     chosen_blue = [i[-1] for i in custom]
    #     chosen_timemark_previous  = [i[0] for i in custom_previous_chosen_reverse]
    #     chosen_blue_previous = [i[-1] for i in custom_previous_chosen_reverse]

    #     # all data
    #     ys_1 = chosen_blue
    #     xs_1 = chosen_timemark
    #     MA_ls = plot_MA(input_average, chosen_blue, chosen_blue_previous)
    #     ys_MA = MA_ls

    # elif style_input == 2:
    #     print('Initializing style 2 ...')

    #     # Processing data
    #     for a in timeframe:
    #         if starting in a:
    #             starting_point = timeframe.index(a)
    #             break
                    
    #     all_chosen_blue = []
    #     for b in range(len(timeframe)):
    #         if starting_point <= b:
    #             all_chosen_blue.append([timeframe[b], timespan[b], percentage[b]])

    #     # We need to find all the blue data first
    #     all_blue_all = []
    #     for c in range(len(timeframe)):
    #         all_blue_all.append([timeframe[c], timespan[c], percentage[c]])

    #     all_blue_previous = []
    #     for i in all_blue_all:
    #         if i not in all_chosen_blue:
    #             all_blue_previous.append(i) 
    #     all_blue_previous.append(all_blue_all[starting_point]) # We need to append the starting point of the chosen data in the end, since it will become the base when we pass this list to our function getPreviousPoint()


    #     custom = getChosenPoints(custom_time, all_chosen_blue)

    #     custom_previous = getChosenPoints(custom_time, all_blue_previous[::-1])
    #     custom_previous_chosen = custom_previous[1:input_average]
    #     custom_previous_chosen_reverse = custom_previous_chosen[::-1]

    #     chosen_timemark = [i[0] for i in custom]
    #     chosen_blue = [i[-1] for i in custom]
    #     chosen_timemark_previous  = [i[0] for i in custom_previous_chosen_reverse]
    #     chosen_blue_previous = [i[-1] for i in custom_previous_chosen_reverse]
    #     MA_ls = plot_MA(input_average, chosen_blue, chosen_blue_previous)

    #     # all data
    #     ys_1 = chosen_blue[:input_range]
    #     xs_1 = chosen_timemark[:input_range]
    #     ys_MA = MA_ls[:input_range]

    message = f'Confirmation: \n- Chosen pair: {pair_input} ... \n- Chosen style: {style_input} ... \n- Starting time: {starting} ... \n- Ending time: {ending} ... \n- No. of bins: {input_range} ... \n- Timeframe: {custom_time} ... \n- Moving average: {input_average} ...'
    print(message)

    return dcc.Graph(id='currency_line', 
        figure={
            'data': [
                {'x':xs_1, 'y': ys_1, 'type':'line', 'name':'percentage'},
                {'x':xs_1, 'y': ys_MA, 'type':'line', 'name':f'MA_{input_average}'},
                ],
            'layout':{
                'title': f'{pair_input}: {custom_time} minutes'
            }}), dcc.Graph(id='currency_bar', 
        figure={
            'data': [
                {'x':xs_1, 'y':ys_1, 'type':'bar', 'name':'percentage'}
                ]
            })

if __name__ == '__main__':
    graph_test.run_server(debug=True,host='0.0.0.0')

