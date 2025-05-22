
import dash
from dash import Dash, html, dcc, page_container, page_registry
import dash_bootstrap_components as dbc  # Import Dash Bootstrap Components

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP]) # Use dbc.themes.BOOTSTRAP

app.layout = html.Div([
    dbc.NavbarSimple(  # Use NavbarSimple for a simple navigation bar
        children=[
            dbc.NavItem(dbc.NavLink(f"{page['name']}", href=page["relative_path"]))
            for page in dash.page_registry.values()
            if page["module"] != "pages.home"  # Exclude home from the navbar
            if page["module"] != "pages.ARIMA_Highlights"  # Exclude home from the navbar
        ],
        brand="Data Analysis and ARIMA Forecasting",  # Set the brand text
        brand_href="/",  # Set the brand link to home page
        color="primary",  # Change the background color to primary (e.g., blue)
        dark=True,  # Set text color to white
        style={'marginBottom': '20px', 'fontFamily': 'Arial'}  # Add some bottom margin for spacing and font
    ),
    dbc.Container(page_container, fluid=True, style={'fontFamily': 'Arial'})  # Wrap page_container in a Container for better layout and font
])

server = app.server


