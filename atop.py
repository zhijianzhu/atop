import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

import flask
from datetime import date

current_time = str(date.today())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

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

data = [ dict(
        type = 'scattergeo',
        #locationmode =  #'USA-states',
        locations="iso_alpha",
        lon = df_conf['Long'],
        lat = df_conf['Lat'],
        text = df_conf['text'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'circle',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            # colorscale = scl,
            color_continuous_scale=px.colors.diverging.BrBG,
            color_continuous_midpoint = median_val,
            cmin = 0,
            color = df_conf['total'],
            cmax = df_conf['total'].max(),
            colorbar=dict(
                title="CoronaVirus Confirmed Total as of " + current_time
            )
        ))]


layout = dict(
        title = 'CoronaVirus Confirmed Total',
        height = 700,
        colorbar = True,
        geo = dict(
            # scope='usa',
            projection= 'natural earth', #dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )

fig = dict( data=data, layout=layout )    

df_deaths['text'] = df_deaths.apply(get_text,axis=1)

scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

median_val_d = df_deaths['total'].median()
data_d = [ dict(
        type = 'scattergeo',
        #locationmode =  #'USA-states',
        locations="iso_alpha",
        lon = df_deaths['Long'],
        lat = df_deaths['Lat'],
        text = df_deaths['text'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'circle',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            color_continuous_scale=px.colors.diverging.Fall,
            color_continuous_midpoint = median_val_d,
            cmin = 0,
            color = df_deaths['total'],
            cmax = df_deaths['total'].max(),
            colorbar=dict(
                title="CoronaVirus Deaths Total as of " + current_time
            )
        ))]


layout_d = dict(
        title = 'CoronaVirus Death Total as of 2020/03/13',
        height = 700,
        colorbar = True,
        geo = dict(
            # scope='usa',
            projection= 'natural earth', #dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )
fig_d = dict( data=data_d, layout=layout_d )    

app.layout  = html.Div([
    dcc.Graph(id='virus_c_graph', figure=fig),
    dcc.Graph(id='virus_d_graph', figure=fig_d)
])

if __name__ == '__main__':
    app.run_server(debug=False, port=5000)
