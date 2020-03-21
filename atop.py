import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import pandas as pd
import numpy as np
import pgeocode


import flask
import utilities as utl
from utilities import colors

from app_layout import layout
from app_callback import register_callbacks

scl = [[0, "rgb(227,26,28)"],
       [0.25, "rgb(251,154,153)"],
       [0.45, "rgb(51,160,44)"],
       [0.65, "rgb(178,223,138)"],
       [0.85, "rgb(31,120,180)"],
       [1, "rgb(166,206,227)"]]

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.title = 'CADSEA 2020'

app.layout = layout
register_callbacks(app)


if __name__ == '__main__':

    app.run_server(debug=False, port=5000)
