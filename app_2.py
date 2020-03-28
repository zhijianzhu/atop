# Data
import pandas as pd
import pickle
# Graphing
import plotly.graph_objects as go
# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

import utilities as utl

# Navbar
from navbar import Navbar

from plotly.validators.scatter.marker import SymbolValidator
raw_symbols = SymbolValidator().values

# navigation bar
nav = Navbar()

header = html.H3(
    'Choose a zipcode and find nearby status.'
)

search = dcc.Input(
    placeholder='Enter a zipcode...',
    type='text',
    value='21044',
    id='search',
    style=dict(display='flex', justifyContent='center'),

)

output_2 = html.Div(id='output_2',
                    children=[],
                    )
def App():
    layout = html.Div([
        nav,
        header,
        search,
        output_2
    ])
    return layout

def plot_figure(zipcode):

    #data_list_confirmed, data_list_deaths, data_list_recovered, date_list, region_of_interest = utl.load_data_2()

    data, date_list = utl.search_by_zipcode(zipcode)

    data = [go.Scatter(x=date_list,
                       y=data,
                       mode="markers+lines",
                       marker_symbol=raw_symbols[0],
                       marker_line_color="red",
                       marker_color="lightskyblue",
                       marker_line_width=2, marker_size=15)]

    graph = dcc.Graph(
        figure={
            'data': data,
            'layout': go.Layout(
                title='{} confirmed case change'.format(zipcode),
                yaxis={'title': 'confirmed case'},
                hovermode='closest'
            )
        }
    )
    return graph


def show_news_list(zipcode):
    news_list = utl.get_local_news_by_zipcode(zipcode)
    
    ol = []
    for news in news_list:
        ol.append([news['title'], news['url']])
        
    # create ol list
    html_ol_list = []

    return html.Ol([html.Li(html.A(x[0], href=x[1])) for x in ol])
                
