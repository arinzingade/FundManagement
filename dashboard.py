from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from components import header

def create_dash_app(flask_app, username = ""):
    
    external_sheets = ["/static/dash_styles/header_style.css"]
    appDash = Dash(__name__, server=flask_app, external_stylesheets=external_sheets, 
                   url_base_pathname='/dashboard/')

    appDash.layout = html.Div([
        dcc.Location(id='/login', refresh=False),
        header.generate_header(username)
    ])

    return appDash
