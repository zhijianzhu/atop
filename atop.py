import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import flask

import app_1
import app_2

from homepage import Homepage


server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=[dbc.themes.UNITED],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.title = 'CADSEA 2020'

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/by_region':
        return app_1.App()
    elif pathname == "/search":
        return app_2.App()
    else:
        return Homepage()

@app.callback(Output('output_1', 'children'),
              [Input('pop_dropdown', 'value')])
def update_graph(city):
    figure_1 = app_1.plot_figure(city)
    return figure_1

@app.callback(Output('output_2', 'children'),
              [Input('search', 'value')])
def update_graph_2(zipcode):
   # figure_2 = app_2.plot_figure(zipcode)
    figure_2 = app_2.show_news_list(zipcode)
    return figure_2


if __name__ == '__main__':
    app.run_server(debug=False, port=5000)
