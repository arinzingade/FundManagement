import dash_bootstrap_components as dbc
from dash import html
from dash import html, dcc

def generate_header(username):
    header = html.Div([
        dbc.Col([
            dcc.Link('Zingade Holdings', href="/login", className="company"),
            ], width=4, className="company-name"),
            
            dbc.Col([
                html.P('Investment Dashboard')
            ], width=4, className="Investment-Dash"),
            
            dbc.Col([
                dbc.NavLink(username, href='/link1', class_name= "user"),
            ], width=4, className="User-Log")
        ], className = "header" )

    return header
