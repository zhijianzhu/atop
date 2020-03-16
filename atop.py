import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly.express as px

import flask
import utilities as utl

from datetime import date

current_time = str(date.today())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)
app.title = 'CADSEA 2020'

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

data_list_confirmed, data_list_deaths, data_list_recovered, date_list, regions_of_interest = utl.load_data()

# print('reading the csv')
df_conf = pd.read_csv('data/time_series_19-covid-Confirmed.csv')
date_cols = [c for c in df_conf.columns if '/20' in c]
df_conf['total'] = df_conf[date_cols].sum(axis=1)
df_conf = df_conf[df_conf['total']>0]

df_deaths = pd.read_csv('data/time_series_19-covid-Deaths.csv')
df_deaths['total'] = df_deaths[date_cols].sum(axis=1)
df_deaths = df_deaths[df_deaths['total']>0]


# print('done reading the csv file')
def get_text(r):
    # print(r['Province/State'])
    if str(r['Province/State'])!='nan': 
        return r['Province/State'] + '<br>' + 'Confirmed: ' + str(r['total'])
    else:
        return r['Country/Region'] + '<br>' + 'Confirmed: ' + str(r['total'])

df_conf['text'] = df_conf.apply(get_text,axis=1)
median_val = df_conf['total'].median()

# scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
#     [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]
scl = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(240, 210, 250)"]]


df_deaths['text'] = df_deaths.apply(get_text,axis=1)

scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

median_val_d = df_deaths['total'].median()


data, layout = utl.config_geo_layout(df_conf, px, median_val, current_time)
fig = dict( data=data, layout=layout)    

data_d, layout_d = utl.config_geo_layout(df_deaths, px, median_val, current_time)
fig_d = dict( data=data_d, layout=layout_d )    

app.layout = html.Div([
    html.H1(
        children='COVID-19 Tracking and Modelling',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
     html.H3(
        children='by CADSEA @2020',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

        
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='By Country/Region', value='tab-1'),
        dcc.Tab(label='Geo Display', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
           html.H3('Confirmed Cases'), 
           dcc.Graph(
            id='Graph1',
            figure={
                'data': data_list_confirmed,
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {'color': colors['text']}
                }
            }
         ),
        
      ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Geo Distribution'),
            
            dcc.Graph(id='virus_c_graph', figure=fig),
            dcc.Graph(id='virus_d_graph', figure=fig_d)
        ])
    
if __name__ == '__main__':
    
    app.run_server(debug=False, port=5000)
