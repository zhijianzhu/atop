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

@app.callback(
    Output('virus_c_graph', 'figure'),
    [Input(component_id='my_zip', component_property='value'),
     Input('radius', 'value'),
     Input('date-slider', 'value')]
)
def update_output_div(zipcode, radius, value):
    # zipcode='20030'
    df_latlong = pd.read_csv('data/lat_long_by_loc_name.csv')

    df_conf = pd.read_csv('data/time_series_19-covid-Confirmed.csv')
    date_cols = [c for c in df_conf.columns if '/20' in c]
    df_conf = df_conf[(df_conf['Country/Region'] == 'US')]  # &(df_conf['Province/State'].str.contains(','))
    df_conf['total'] = df_conf[date_cols].sum(axis=1)
    df_conf = df_conf[df_conf['total'] > 0]
    df_conf = df_conf.drop(['Lat', 'Long'], 1)
    df_conf = df_conf.merge(df_latlong, on='Province/State')

    nomi = pgeocode.Nominatim('us')
    zipinfo = nomi.query_postal_code(zipcode)
    dist_vals = df_conf.apply(utl.row_dist, axis=1, zipinfo=zipinfo)
    df_local = df_conf[dist_vals <= int(radius)]
    df_local_day = df_local[df_local[date_cols[value]] > 0]
    # count_local = df_local_day.sum()
    dis_test = df_local_day.apply(utl.get_disp_text, axis=1, ty='Confirmed', col=date_cols[value])
    # print(df_local_day.shape)
    # print('zipcode: {}, date:{}'.format(zipcode, date_cols[value]))
    data = [dict(
        type='scattergeo',
        locationmode='USA-states',
        showland=True,
        center=dict(lon=zipinfo['longitude'], lat=zipinfo['latitude']),
            lataxis_range=[-50, 20],
            lonaxis_range=[0, 200],
            # locations="iso_alpha",
            lon=df_local_day['Long'],
            lat=df_local_day['Lat'],
            text=dis_test,
            mode='markers',
            marker=dict(
                size=8,
                opacity=0.8,
                reversescale=True,
                autocolorscale=False,
                symbol='circle',
                line=dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale=scl,
                cmin=0,
                color=df_local_day[date_cols[value]],
                cmax=df_local_day[date_cols[value]].max(),
                colorbar=dict(
                    title="CoronaVirus Confirmed on %s" % (date_cols[value])
                )
        ))]

    layout = dict(
        title='CoronaVirus Confirmed Daily',
        height=700,
        colorbar=True,
        geo=dict(
            scope='usa',
            projection='natural earth',  # dict( type='albers usa' ),
            showland=True,
            landcolor="rgb(250, 250, 250)",
            subunitcolor="rgb(217, 217, 217)",
            countrycolor="rgb(217, 217, 217)",
            countrywidth=0.5,
            subunitwidth=0.5
        ),
    )
    return {'data': data, 'layout': layout}


if __name__ == '__main__':

    app.run_server(debug=False, port=5000)
