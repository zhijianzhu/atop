import pandas as pd

import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from navbar import Navbar

from init import app

from src.dataService import dataServiceCSBS as CSBS


from plotly.validators.scatter.marker import SymbolValidator
raw_symbols = SymbolValidator().values

nav = Navbar()


header = html.H3(
    'Select a region/country name!'
)


def load_options():
    ds = CSBS()

    # data_list_confirmed, data_list_deaths, data_list_recovered, date_list, region_of_interest = utl.load_data_2()
    region_of_interest = ds.regions()
    options = [{'label': x, 'value': x} for x in region_of_interest]
    defaults = region_of_interest[:7]

    return options, defaults


region_options, region_defaults = load_options()

dropdown = html.Div(dcc.Dropdown(
    id='Region_of_interest',
    options=region_options,
    value=region_defaults,
    multi=True

))

radioItems = html.Div([
    html.Label('Time Window', id='time_range'),
    dcc.RadioItems(
        id='tab1_TimeWindow',
        options=[
            {'label': 'All', 'value': 'ALL'},
            {'label': 'Last Month', 'value': 'MON'},
            {'label': 'Last Two Weeks', 'value': 'WEEKS'},
            {'label': 'Last Week', 'value': 'WEEK'},
        ],
        value='ALL'
    )
])


confirmedGraph = html.Div(id='comfirmed_region_graph',
                          children=[],
                          )
deathsGraph = html.Div(id='deaths_region_graph',
                       children=[],
                       )


def App():
    layout = html.Div([
        nav,
        header,
        dropdown,
        radioItems,
        confirmedGraph,
        deathsGraph,

    ])
    return layout


@app.callback(
    [Output(component_id='comfirmed_region_graph', component_property='children'),
     Output(component_id='deaths_region_graph', component_property='children'),
     Output(component_id='time_range', component_property='children'),
     ],
    [Input(component_id='tab1_TimeWindow', component_property='value'),
     Input('Region_of_interest', 'value')])
def update_graph(date_window_option, region_of_interest):
    ds = CSBS()
    dt_range = ds.date_range_str(date_window_option)

    confirmed = ds.refresh_category(
        'Confirmed',
        date_window_option,
        region_of_interest)
    deaths = ds.refresh_category(
        'Deaths',
        date_window_option,
        region_of_interest)

    return plot_figure(confirmed, 'Confirmed', dt_range), \
        plot_figure(deaths, 'Deaths', dt_range), \
        'Time Window:{}'.format(dt_range)


def plot_figure(df, category, dt_range):

    graph = dcc.Graph(
        figure={
            'data': df,  # data,
            'layout': go.Layout(
                title='{} cases change over date<br>{}'.format(
                    category, dt_range),
                yaxis={'title': 'Population'},
                hovermode='closest'
            )
        }
    )
    return graph
