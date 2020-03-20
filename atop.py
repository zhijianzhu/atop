import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import pandas as pd
import numpy as np

import flask
import utilities as utl
from utilities import colors

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]


server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.title = 'CADSEA 2020'

app.layout = html.Div([

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

])

@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return utl.tab_1_layout()
    elif tab == 'tab-2':
        return utl.tab_2_layout()
    elif tab == 'tab-3':
        return utl.tab_3_layout()
    elif tab == 'tab-4':
        return utl.tab_4_layout()


if __name__ == '__main__':

    app.run_server(debug=False, port=5000)
