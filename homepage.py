import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import utilities as utl

from navbar import Navbar
nav = Navbar()


def load_date_list():
    data_list_confirmed, data_list_deaths, data_list_recovered, date_list, region_of_interest = utl.load_data_2()
    return date_list

def load_case_list(region="US"):
    data_list_confirmed, data_list_deaths, data_list_recovered, date_list, region_of_interest = utl.load_data_2()
    return data_list_confirmed[region]


layout = {
    'plot_bgcolor': utl.colors['background'],
    'paper_bgcolor': utl.colors['background'],
    'font': {'color': utl.colors['text']}
}

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Heading 1"),
                        html.P(
                            """
                            This coronavirus is changing the world dramatically.
                            """
                        ),
                        dbc.Button("View details", color="secondary"),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.H2("Confirmed cases"),
                        dcc.Graph(
                            figure={"data": [
                                {"x": load_date_list(), "y": load_case_list("US"), 'mode': "lines+markers", 'name': 'US'},
                                {"x": load_date_list(), "y": load_case_list("Italy"), 'mode': "lines+markers", 'name': 'Italy'}

                            ],
                                "layout": layout
                            }
                        ),
                    ]
                ),
            ]
        ),

    ],
    className="mt-4",
)

def Homepage():
    layout = html.Div([
        nav,
        body
    ])
    return layout


if __name__ == "__main__":

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
    app.layout = Homepage()
    app.run_server()
