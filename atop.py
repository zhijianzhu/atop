import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# layout
import page_by_region
import page_search
import page_model

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
        return page_by_region.App()
    elif pathname == "/search":
        return page_search.App()
    elif pathname == "/model":
        return page_model.load_layout()
    else:
        return Homepage()


# @app.callback(Output('output_2', 'children'),
#               [Input('search', 'value')])
# def update_graph_zipcode(zipcode):
#     figure_2 = page_search.plot_figure(zipcode)
#     return figure_2


# @app.callback(Output('output_22', 'children'),
#               [Input('search', 'value')])
# def update_graph_zipcode2(zipcode):
#     news_list = page_search.show_news_list(zipcode)
#     return news_list


if __name__ == '__main__':
    app.run_server(debug=False, port=5000)
