import os

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np

df_Confirmed = pd.read_csv("data/time_series_19-covid-Confirmed.csv")
df_Deaths = pd.read_csv("data/time_series_19-covid-Deaths.csv")
df_Recovered = pd.read_csv("data/time_series_19-covid-Recovered.csv")


countries = df_Confirmed['Country/Region'].unique()

date_list = df_Confirmed.columns.to_list()
date_list = date_list[4:]

df =  df_Confirmed[df_Confirmed['Country/Region']=='Mainland China']
df_1 =  df[df['Province/State']=='Hubei']
df_2 =  df[df['Province/State']=='Anhui']

df =  df_Confirmed[df_Confirmed['Country/Region']=='US']

df = df.fillna(0)
confirmed_number = np.sum(np.array(df[date_list]),axis=0)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello World',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='COVID-19 Tracking and Modelling', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
              #  {'x': date_list, 'y': list(np.array(df_1[date_list])[0]), 'type': 'bar', 'name': 'Wuhan'},
                {'x': date_list, 'y': list(confirmed_number), 'mode': 'lines+markers', 'name': 'USA'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0",debug=True,port=5000)
