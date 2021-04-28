import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import statistics as sts
import pandas as pd
from mongo_data import *
from graphs import *
print('Done importing!')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
graph_test = dash.Dash(__name__, external_stylesheets=external_stylesheets)

graph_test.layout = html.Div(children=[

    html.Div([
        html.Div([
            html.B('Please select one of the following currency pairs: '),
            html.Div('AUD_USD, EUR_JPY, EUR_USD, GBP_USD'),
            dcc.Input(id='pair_input', type='text', value='', placeholder='Enter a pair ...', debounce=True),
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
        ], style={"margin-top": "20px"}),

        html.Div([
            html.B('Please select the ending time'),
            html.Div('(eg. YYYY-MM-DD hh:mm)'),
            dcc.Input(id='ending', type='text', value='', placeholder='Enter a value ...', debounce=True),
        ], style={"margin-top": "20px"}),

        html.Div([
            html.B('Please select the chart range'),
            html.Div('(eg. 10bins, 20bins)'),
            dcc.Input(id='input_range', type='number', value='', placeholder='Enter a value ...', debounce=True),
        ], style={"margin-top": "20px"}),

        html.Div([
            html.B('Please select the timeframe'),
            html.Div('(eg. 1min, 5min, 1440min)'),
            dcc.Input(id='custom_time', type='number', value='', placeholder='Enter a value ...', debounce=True),
        ], style={"margin-top": "20px"}),

        html.Div([
            html.B('Please select the moving average period'),
            html.Br(),
            dcc.Input(id='input_average', type='number', value='', placeholder='Enter a value ...', debounce=True),
        ], style={"margin-top": "20px"})

     ], style={'columnCount': 2}),

    html.Div(id='style_output')
])

@graph_test.callback(
    Output(component_id="style_output", component_property="children"),
    [Input(component_id="pair_input", component_property="value"),    
    Input(component_id="style_input", component_property="value"),
    Input(component_id="starting", component_property="value"),
    Input(component_id="ending", component_property="value"),
    Input(component_id="input_range", component_property="value"),
    Input(component_id="custom_time", component_property="value"),
    Input(component_id="input_average", component_property="value")]
)

def update_data(pair_input, style_input, starting, ending, input_range, custom_time, input_average):
    xs_1 = []
    ys_1 = []
    ys_MA = []
    ending_point = -1
    starting_point = 0
    collection = ''
    timeframe, timespan, percentage = PullfromMongoDB(pair_input, collection)
    xs_1, ys_1, ys_MA = plotChart(pair_input, style_input, starting, ending, input_range, custom_time, input_average, starting_point, ending_point, xs_1, ys_1, ys_MA, timeframe, timespan, percentage)
    ys_100 = [100 for i in range(len(xs_1))]

    message = f'Confirmation: \n- Chosen pair: {pair_input} ... \n- Chosen style: {style_input} ... \n- Starting time: {starting} ... \n- Ending time: {ending} ... \n- No. of bins: {input_range} ... \n- Timeframe: {custom_time} ... \n- Moving average: {input_average} ...'
    print(message)

    graph_1 = dcc.Graph(id='currency_line', 
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
                            }), dcc.Graph(id='currency_line_base', 
                        figure={
                            'data': [
                                {'x':xs_1, 'y': ys_1, 'type':'line', 'name':'percentage'},
                                {'x':xs_1, 'y': ys_100, 'type':'bar', 'name':f'100%'},
                                ]
                            })

    return graph_1

if __name__ == '__main__':
    graph_test.run_server(debug=True,host='0.0.0.0')

