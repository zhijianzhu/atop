import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly_express as px

from init import app

from .dataService import ds as ds

layout = html.Div([
    html.Label('Geo Distribution'),

    dcc.Graph(
        id='Geo_confirmed',
        # figure=organize_figure_structure(data_list_confirmed)
        figure=dict(data=ds.geo_data('Confirmed'),
                    layout=ds.geo_layout('Confirmed Total'))
    ),
    dcc.Graph(
        id='Graph_death',
        # figure=utl.organize_figure_structure(data_list_deaths)
        figure=dict(data=ds.geo_data('Deaths'),
                    layout=ds.geo_layout('Deaths Total'))
    ),
])
