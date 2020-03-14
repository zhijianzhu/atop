import os

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

import flask
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import datetime
from datetime import date

current_time =  str(datetime.datetime.now())
current_time = str(date.today())

df_Confirmed = pd.read_csv("data/time_series_19-covid-Confirmed.csv")
df_Deaths = pd.read_csv("data/time_series_19-covid-Deaths.csv")
df_Recovered = pd.read_csv("data/time_series_19-covid-Recovered.csv")

countries = df_Confirmed['Country/Region'].unique()

date_list = df_Confirmed.columns.to_list()
date_list = date_list[4:]

df =  df_Confirmed[df_Confirmed['Country/Region']=='Mainland China']
df_1 =  df[df['Province/State']=='Hubei']
df_2 =  df[df['Province/State']=='Anhui']


region_of_interest = ['US','Germany','Italy','United Kingdom','Canada']

def update_number_by_region(df = df_Confirmed):
    data_list=[]
    
    for region in region_of_interest:
        df =  df[df['Country/Region']== region]
        df = df.fillna(0)
        confirmed_number = list(np.sum(np.array(df[date_list]),axis=0))
        data_list.append({'x': date_list, 'y': confirmed_number, 'mode': 'lines+markers', 'name': region})
        
    return data_list
    
data_list_confirmed = update_number_by_region(df_Confirmed)
data_list_deaths = update_number_by_region(df_Deaths)
data_list_recovered = update_number_by_region(df_Recovered)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='COVID-19 Tracking and Modelling' + "\n" +current_time,
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Confirmed', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': data_list_confirmed,
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),

])


if __name__ == "__main__":
    app.run_server(host="0.0.0.0",debug=True, port=5000)
    #app.run(host='0.0.0.0')

