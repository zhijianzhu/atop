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

def compute_increase_rate(region='US'):
    data_list_confirmed, date_list = utl.load_data_3(region)
    A = data_list_confirmed
    print("confirmed data is ", A)
    rate = [(A[k+1] - A[k])/A[k]*100 for k in range(0, len(A)-1)]
    return rate

def load_date_list_2(region='US'):
    data_list_confirmed, date_list = utl.load_data_3(region)
    print("region is ", region, " date_list is ", date_list)
    return date_list[1:]


body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Covid 19 Status"),
                        html.P(
                            """
                            This coronavirus spreading is changing the world dramatically.
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
                                {"x": load_date_list(), "y": load_case_list("Italy"), 'mode': "lines+markers", 'name': 'Italy'},

                            ],
                                "layout": utl.layout
                            }
                        ),
                    ]
                ),
            ]
        ),

        dbc.Row(
            [


                dbc.Col(
                    [
                        html.H2("US daily increase rate"),
                        dcc.Graph(
                            figure={"data": [
                                {"x": load_date_list_2("US"), "y": compute_increase_rate("US"), 'mode': "lines+markers", 'name': 'US'},

                            ],
                                "layout": utl.layout
                            }
                        ),
                    ]
                ),


                dbc.Col(
                    [
                        html.H2("Italy daily increase rate"),
                        dcc.Graph(
                            figure={"data": [
                                {"x": load_date_list_2("Italy"), "y": compute_increase_rate("Italy"), 'mode': "lines+markers", 'name': 'Italy'},

                            ],
                                "layout": utl.layout
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
