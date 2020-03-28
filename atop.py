import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# layout
import app_1
import app_2
import app_3

from homepage import Homepage


from init import app, server  


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
        return app_3.load_layout()

@app.callback(Output('output_1', 'children'),
              [Input('pop_dropdown', 'value')])
def update_graph_1(city):
    figure_1 = app_1.plot_figure(city)
    return figure_1

@app.callback(Output('output_2', 'children'),
              [Input('search', 'value')])
def update_graph_2(zipcode):
    figure_2 = app_2.plot_figure(zipcode)
    return figure_2


@app.callback(Output('output_22', 'children'),
              [Input('search', 'value')])
def update_graph_22(zipcode):
    news_list = app_2.show_news_list(zipcode)
    return news_list

if __name__ == '__main__':
    app.run_server(debug=False, port=5000)
