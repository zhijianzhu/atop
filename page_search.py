import math 
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

from dash.dependencies import Output, Input

from src.geoService  import geoClass 
from src.newsService import newsClass 

from init import app
import utilities as utl

# Navbar
from navbar import Navbar

from plotly.validators.scatter.marker import SymbolValidator

raw_symbols = SymbolValidator().values


# navigation bar
nav = Navbar()
geoSvr  = geoClass() 
newsSvr = newsClass()

header = html.H3(
    'Choose a zipcode and find nearby status.'
)

zipcodeInput = dcc.Input(
    placeholder='Enter a zipcode...',
    type='text',
    value='21044',
    id='zipcodeInput',
    style=dict(display='flex', justifyContent='center'),
)

radiusInput = dcc.Input(
    placeholder='Enter a radius(miles)...',
    type='text',
    value='100',
    id='radiusInput',
    style=dict(display='flex', justifyContent='center'),
)


confirmedNearby = html.Div( id='confirmedNearby',  )

deathsNearby = html.Div(id='deathsNearby',  )

localNews = html.Div(id = 'localNews' )


def App():
    layout = html.Div([
        nav,
        header,
        zipcodeInput,
        radiusInput,
        html.H3('Confirmed Cases') ,
        confirmedNearby,
        html.H3("Deaths cases"),
        deathsNearby,
        html.H3("Related news"),
        localNews
    ])
    return layout



@app.callback(
    [Output(component_id='confirmedNearby', component_property='children'),
     Output(component_id='deathsNearby', component_property='children'),
     Output(component_id='localNews', component_property='children'),
         ],
    [Input(component_id='zipcodeInput', component_property='value'),
     Input('radiusInput', 'value')])
def update_map_and_news( zipcode, radius):

    return plot_figure('Confirmed',zipcode, radius), \
           plot_figure('Deaths',zipcode, radius), \
           newsSvr.show_news_list(zipcode)


def plot_figure(category, zipcode, radius):

    df = geoSvr.geo_data(category, zipcode, radius)

    fig = px.scatter_mapbox(df,
        lat = 'Latitude', lon = 'Longitude', 
        hover_name = 'County_Name',
        hover_data=[category],
        size = category, 
        # color_discrete_sequence=['fuchsia'],
        zoom=geoSvr.zoom,
        center=geoSvr.center.dict(), 
        height = 420
        )

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={ 'r':10, 't':10, 'l':10, 'b':10, })
    fig.update_layout(autosize=True)
    fig.update_layout( )

    graph = dcc.Graph(
            figure=fig ,
            )
    return graph
