import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# import plotly.graph_objs as go
# import pandas as pd
# import numpy as np

import utilities as utl
# from utilities import colors

from init import app, server  
from src import tab1_byCountryRegion as tab_1 
from src import tab2_GeoDisplay as tab_2

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
        return tab_1.layout 
    elif tab == 'tab-2':
        return tab_2.layout 
    elif tab == 'tab-3':
        return None
    elif tab == 'tab-4':
        return None



if __name__ == '__main__':

    app.run_server(debug=False, port=5000)
