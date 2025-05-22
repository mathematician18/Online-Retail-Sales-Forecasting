
import dash
from dash import html, dcc, page_container, page_registry
import dash_bootstrap_components as dbc

# SI se refactorizara, no es necesario registrarla como página ya que solo será contenido de un modal
dash.register_page(__name__, path="/ARIMA_Highlights", name="ARIMA_Highlights", title="ARIMA_Highlights")


# Define layout with Bootstrap components for styling
layout = dbc.Container([
    html.Strong("ARIMA Model Highlights", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'marginLeft': '1.2em'}),
                html.Br(),
                html.P(
                    "The ARIMA model effectively captures trends and seasonal patterns. Key findings include:",
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'marginLeft': '1.2em'} 
                ),
                dbc.ListGroup([
                    dbc.ListGroupItem(
                        "Significant moving average terms indicate their importance.",  className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}
                    ),
                    dbc.ListGroupItem(
                        "Non-significant autoregressive terms suggest potential simplification.",  className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}
                    ),
                    dbc.ListGroupItem(
                        "Tests indicate absence of autocorrelation but issues with normality and variance.",  className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}
                    ),
                     dbc.ListGroupItem(
                        "Singular covariance matrix warning indicates potential numerical issues.",  className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem',  'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}
                    ),
                ],  flush=True)
            ], className="mb-2")

# esta es la refactirizacion que no se ocupo por generar error
#def get_arima_highlights_layout():
#    layout = dbc.Container([
#        html.Strong("ARIMA Model Highlights", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'marginLeft': '1.2em'}),
#        html.Br(),
#        html.P(
#            "The ARIMA model effectively captures trends and seasonal patterns. Key findings include:",
#            style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'marginLeft': '1.2em'}
#        ),
#        dbc.ListGroup([
#            dbc.ListGroupItem(
#                "Significant moving average terms indicate their importance.",  className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}
#            ),
#            dbc.ListGroupItem(
#                "Non-significant autoregressive terms suggest potential simplification.",  className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}
#            ),
#            dbc.ListGroupItem(
#                "Tests indicate absence of autocorrelation but issues with normality and variance.",  className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}
#            ),
#            dbc.ListGroupItem(
#               "Singular covariance matrix warning indicates potential numerical issues.",  className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem',  'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}
#            ),
#        ],  flush=True)
#    ], className="mb-2") # className="mb-2" estaba en un dbc.Container que ya no es el principal aquí, ajustar si es necesario.
#                        # Para el modal, el dbc.Container podría no ser necesario o necesitar diferentes clases.
#                        # Por simplicidad, lo mantendré, pero el estilo podría necesitar ajustes dentro del modal.
#    return layout

# Si este archivo solo define el layout para el modal, el siguiente 'layout = ...' no es necesario.
# layout = get_arima_highlights_layout() # Esto sería si se ejecutara como página independiente

