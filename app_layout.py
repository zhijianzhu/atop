import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd


df_conf = pd.read_csv('data/time_series_19-covid-Confirmed.csv')
date_cols = [c for c in df_conf.columns if '/20' in c]

layout = html.Div([

    html.H1(
        children='COVID-19 Tracking and Modelling',
        style={
            'textAlign': 'center',
            'color': 'blue'
        }
    ),

    html.H6(
        children='by CADSEA @2020',
        style={
            'textAlign': 'center',
            'color': 'black'
        }
    ),

    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='By Country/Region', value='tab-1'),
        dcc.Tab(label='Geo Display', value='tab-2'),
        dcc.Tab(label='Search', value='tab-3'),
        dcc.Tab(label='Modelling/Predicting', value='tab-4'),

    ]),
    html.Div(id='tabs-content'),

    html.Div([
        dcc.Markdown('''
        ### Please slide to choose a date. ###
    '''),

        dcc.Slider(
            id='date-slider',
            min=0,
            max=len(date_cols) - 1,
            step=None,
            marks=dict((i, d) if i % 5 == 0 else (str(i), '') for i, d in enumerate(date_cols)),
            value=len(date_cols) - 1,
        ),
    ]),
    html.Div([
        dcc.Markdown('### Please enter a zip code and input a radius (miles) ###'),
        dcc.Input(id='my_zip', value='10010', type='text'),
        html.Br(),
        dcc.Input(id='radius', value=1000, type='number'),
        # html.Label(children=' Miles'),
        html.Div(id='count_local'),
        dcc.Graph(id='virus_c_graph'),

        #  dcc.Graph(id='virus_d_graph', figure=fig_d),
    ])

])
