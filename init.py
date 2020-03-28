import dash
import flask
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.config.suppress_callback_exceptions = True

app.title = 'CADSEA 2020'
