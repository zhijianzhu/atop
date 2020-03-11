import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

import pandas as pd
import numpy as np

#df = pd.read_csv('https://ndownloader.figsh.com/files/8261349')

df_Confirmed = pd.read_csv("data/time_series_19-covid-Confirmed.csv")
df_Deaths = pd.read_csv("data/time_series_19-covid-Deaths.csv")
df_Recovered = pd.read_csv("data/time_series_19-covid-Recovered.csv")


countries = df_Confirmed['Country/Region'].unique()

date_list = df_Confirmed.columns.to_list()
date_list = date_list[4:]

df =  df_Confirmed[df_Confirmed['Country/Region']=='Mainland China']
df_1 =  df[df['Province/State']=='Hubei']
df_2 =  df[df['Province/State']=='Anhui']


app = dash.Dash()

app = dash.Dash()
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
                {'x': date_list, 'y': list(df_1[date_list]), 'type': 'bar', 'name': 'Wuhan'},
                {'x': date_list, 'y': list(df_1[date_list]), 'type': 'bar', 'name': 'Anhui'},
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
    
if __name__ == '__main__':
    app.run_server(debug=True)