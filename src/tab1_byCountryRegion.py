import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from init import app

from .dataService import ds as ds
# By Country/Region

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


layout = html.Div([
    html.Label('Region of Interest'),
    dcc.Dropdown(
        id='tab1_Region_of_interest',
        options=[{'label': r, 'value': r} for r in ds.regions()],
        value=ds.regions()[:7],
        multi=True
    ),

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
    ),

    html.H3(children='Confirmed cases',
            style={'textAlign': 'center', 'color': colors['text']}
            ),

    dcc.Graph(
        id='Graph_confirmed',
        # figure=organize_figure_structure(data_list_confirmed)
    ),

    html.H3(children='Death cases',
            style={'textAlign': 'center', 'color': colors['text']}
            ),

    dcc.Graph(
        id='Graph_death',
        #        figure=utl.organize_figure_structure(data_list_deaths)
    ),

    html.H3(children='Recovered cases',
            style={'textAlign': 'center', 'color': colors['text']}
            ),

    dcc.Graph(
        id='Graph_recovered',
        #       figure=utl.organize_figure_structure(data_list_recovered)
    )
])


def organize_figure_structure(data):

    figure_data = {
        'data': data,
        'layout': {
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {'color': colors['text']}
        }
    }

    return figure_data


@app.callback(
    [Output(component_id='Graph_confirmed', component_property='figure'),
     Output(component_id='time_range', component_property='children'),
     ],
    [Input(component_id='tab1_TimeWindow', component_property='value'),
     Input('tab1_Region_of_interest', 'value')])
def update_graph_confirmed(date_window_option, region_of_interest):

    dt_range = ds.date_range_str(date_window_option)
    confirmed = ds.refresh_catetgory('Confirmed', date_window_option, region_of_interest)

    return organize_figure_structure(confirmed), 'Time Window:{}'.format(dt_range)


@app.callback(
    Output(component_id='Graph_recovered', component_property='figure'),
    [Input(component_id='tab1_TimeWindow', component_property='value'),
     Input('tab1_Region_of_interest', 'value')])
def update_graph_recovered(date_window_option, region_of_interest):

    if 'Recovered' not in ds.categories:
        return None

    Recovered = ds.refresh_catetgory('Recovered', date_window_option, region_of_interest)
    return organize_figure_structure(Recovered)


@app.callback(
    Output(component_id='Graph_death', component_property='figure'),
    [Input(component_id='tab1_TimeWindow', component_property='value'),
     Input('tab1_Region_of_interest', 'value')])
def update_graph_death(date_window_option, region_of_interest):

    death = ds.refresh_catetgory('Deaths', date_window_option, region_of_interest)

    return organize_figure_structure(death)
