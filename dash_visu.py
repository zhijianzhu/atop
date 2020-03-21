import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import dash_html_components as html
import pgeocode
import math
from dash.dependencies import Input, Output

def get_disp_text(r, ty, col):
    # print(r['Province/State'])
    if str(r['Province/State']) != 'nan':
        return r['Province/State'] + '<br>' + '%s: ' % ty + str(r[col])
    else:
        return r['Country/Region'] + '<br>' + '%s: ' % ty + str(r[col])

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 3959  # mile

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

def row_dist(r, zipinfo):
    dist = distance((zipinfo['latitude'], zipinfo['longitude']), (r['Lat'], r['Long']))
    return dist


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# print('reading the csv')
df_latlong = pd.read_csv('data/lat_long_by_loc_name.csv')

df_conf = pd.read_csv('data/time_series_19-covid-Confirmed.csv')
date_cols = [c for c in df_conf.columns if '/20' in c]
df_conf = df_conf[(df_conf['Country/Region'] == 'US')]  # &(df_conf['Province/State'].str.contains(','))
df_conf['total'] = df_conf[date_cols].sum(axis=1)
df_conf = df_conf[df_conf['total'] > 0]
df_conf = df_conf.drop(['Lat', 'Long'], 1)
df_conf = df_conf.merge(df_latlong, on='Province/State')

df_deaths = pd.read_csv('data/time_series_19-covid-Deaths.csv')
df_deaths = df_deaths[(df_deaths['Country/Region'] == 'US')]  # &(df_deaths['Province/State'].str.contains(','))

df_deaths['total'] = df_deaths[date_cols].sum(axis=1)
df_deaths = df_deaths[df_deaths['total'] > 0]

# print('done reading the csv file')
def get_text(r):
    # print(r['Province/State'])
    if str(r['Province/State']) != 'nan':
        return r['Province/State'] + '<br>' + 'Confirmed: ' + str(r['total'])
    else:
        return r['Country/Region'] + '<br>' + 'Confirmed: ' + str(r['total'])


df_conf['text'] = df_conf.apply(get_text, axis=1)
median_val = df_conf['total'].median()


scl = [[0, "rgb(227,26,28)"],
       [0.25, "rgb(251,154,153)"],
       [0.45, "rgb(51,160,44)"],
       [0.65, "rgb(178,223,138)"],
       [0.85, "rgb(31,120,180)"],
       [1, "rgb(166,206,227)"]]


df_deaths['text'] = df_deaths.apply(get_text, axis=1)


median_val_d = df_deaths['total'].median()
data_d = [dict(
    type='scattergeo',
    # locationmode =  #'USA-states',
    locations="iso_alpha",
    showcountries=True,
    lon=df_deaths['Long'],
    lat=df_deaths['Lat'],
    text=df_deaths['text'],
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
        # color_continuous_midpoint = median_val_d,
        cmin=0,
        color=df_deaths['total'],
        cmax=df_deaths['total'].max(),
        colorbar=dict(
            title="CoronaVirus Deaths Total as of 2020/03/13"
        )
    ))]


layout_d = dict(
    title='CoronaVirus Death Total as of 2020/03/13',
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
fig_d = dict(data=data_d, layout=layout_d)

app.layout = html.Div([
    html.Div([
        dcc.Markdown('''
        ### Please slide to choose a date. ###
    '''),

        dcc.Slider(
            id='date-slider',
            min=0,
            max=len(date_cols) - 1,
            step=None,
            marks=dict((i, d) if i % 5 == 0 else (str(i), '') for i, d in enumerate(date_cols)),
            value=len(date_cols) - 1,
        ),
    ]),
    html.Div([
        dcc.Markdown('### Please enter a zip code and input a radius (miles) ###'),
        dcc.Input(id='my_zip', value='10010', type='text'),
        html.Br(),
        dcc.Input(id='radius', value=1000, type='number'),
        # html.Label(children=' Miles'),
        html.Div(id='count_local'),
        dcc.Graph(id='virus_c_graph'),

        dcc.Graph(id='virus_d_graph', figure=fig_d),
    ])
])

@app.callback(
    Output('virus_c_graph', 'figure'),
    [Input(component_id='my_zip', component_property='value'),
     Input('radius', 'value'),
     Input('date-slider', 'value')]
)
def update_output_div(zipcode, radius, value):
    # zipcode='20030'
    nomi = pgeocode.Nominatim('us')
    zipinfo = nomi.query_postal_code(zipcode)
    dist_vals = df_conf.apply(row_dist, axis=1, zipinfo=zipinfo)
    df_local = df_conf[dist_vals <= int(radius)]
    df_local_day = df_local[df_local[date_cols[value]] > 0]
    # count_local = df_local_day.sum()
    dis_test = df_local_day.apply(get_disp_text, axis=1, ty='Confirmed', col=date_cols[value])
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
    app.run_server(debug=False)
