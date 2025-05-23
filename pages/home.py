
import dash
from dash import html, dcc, page_container, page_registry
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/", name="ARIMA Sales Forecasting", title="ARIMA Sales Forecasting")

# Define layout with Bootstrap components for styling
layout = dbc.Container([
    html.Link(  # Add this to include custom CSS
        rel='stylesheet',
        href='/assets/list_group_bullets.css'
    ),
    dbc.Row([
        dbc.Col([
            html.Div([
                #html.H1("Sales Forecasting with ARIMA", className="text-center mb-2",
                #        style={'fontFamily': 'Arial', 'fontSize': '1.8rem', 'color': 'white'}),
                html.P("This project demonstrates sales data analysis and forecasting using ARIMA models within a Big Data context.",
                #    className="lead text-center",
                    style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'color': '#cccccc', 'marginLeft': '1.2em'} # Indent
                ),
                html.Hr(className="my-2", style={'borderTop': '1px solid #444'}),
            ], className="mb-2"),
        ], width=12),
    ]),


    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2("Project Overview", style={'fontFamily': 'Arial', 'fontSize': '1.3rem', 'color': 'white'}),
                html.P(
                    ("In today’s dynamic e-commerce landscape, making informed decisions requires both a deep "
                    "understanding of historical business performance and the ability to anticipate future trends. "
                    "This project brings together two fundamental pillars of retail data analytics:"),  # Corrección: uní las dos cadenas para que sea un solo hijo de html.P
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'marginLeft': '1.2em'}  # Indent
                ),
                dbc.ListGroup([
                    dbc.ListGroupItem([
                        html.Strong("Exploratory Data Analysis (EDA)"),
                        " to uncover patterns, segments, and opportunities for improvement in historical and current data."
                    ], className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem([
                        html.Strong("Sales Forecasting"),
                         " using ARIMA models to project future demand and support strategic planning."
                     ], className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                ], flush=True)
            ], className="mb-2"),

            html.Div([
                html.H2("Objective", style={'fontFamily': 'Arial', 'fontSize': '1.3rem', 'color': 'white'}),
                html.P(
                    ("The main goal was to build a comprehensive solution for visualizing, analyzing, and "
                    "forecasting the sales behavior of an online store. To achieve this, we combined Big "
                    "Data tools (Spark, Google BigQuery), advanced analytics (Python, statsmodels), and interactive visualization (Dash)."),  
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'marginLeft': '1.2em'}  
                ),
            ], className="mb-2"),

            html.Div([
                html.H2("1. Exploratory Data Analysis (EDA)", style={'fontFamily': 'Arial', 'fontSize': '1.3rem', 'color': 'white'}),
                html.P(
                    ("The first step involved cleaning, transforming, and enriching historical data on sales, "
                    "customers, and products, stored in Google BigQuery and processed with Spark. An "
                    "interactive Dash dashboard was developed to enable:"), 
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'marginLeft': '1.2em'}  # Indent
                ),
                dbc.ListGroup([
                    dbc.ListGroupItem("Visualization of total revenue, unique customers, and average ticket size by country and period.", className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem("Identification of best-selling products and top revenue generators.", className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem("Analysis of monthly sales evolution to detect trends and seasonality.", className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem("Exploration of purchase patterns by weekday and hour using heat maps.", className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem("Filtering and segmentation of information by country and month, facilitating both operational and strategic decision-making.", className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                ], flush=True),

                html.Br(),
                html.P(
                    ("This analysis helped identify growth opportunities, optimize promotions, and gain a "
                    "deeper understanding of customer behavior, laying the groundwork for more accurate forecasting."), 
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'marginLeft': '1.2em'}  # Indent
                ),
            ], className="mb-2"),

            html.Div([
                html.H2("2. Sales Forecasting with ARIMA", style={'fontFamily': 'Arial', 'fontSize': '1.3rem', 'color': 'white'}),
                html.P(
                    ("Building on the preprocessed data, an ARIMA model was implemented to forecast daily sales. "
                    "The model was tuned and evaluated, taking into account the seasonality and trends identified during the EDA. The dashboard allows users to:"), 
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'marginLeft': '1.2em'}  # Indent
                ),
                dbc.ListGroup([
                    dbc.ListGroupItem("Visualize the historical sales series alongside forecasts for upcoming months.", className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem("Adjust the prediction horizon interactively.", className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem("Review model metrics and diagnostics (parameter significance, residual tests, etc.).", className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem("Interpret results and limitations, highlighting areas for further improvement.", className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    ], flush=True),
                
                html.Br(),
                html.H2("Conclusion", style={'fontFamily': 'Arial', 'fontSize': '1.2rem', 'color': 'white'}),
                html.P(
                    "Integrating exploratory analysis and forecasting within a single dashboard enables users to understand both the past and present of the business, " 
                    "as well as anticipate the future. This synergy between EDA and predictive modeling empowers data-driven decision-making, optimizing the management and growth of the online store.",
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'marginLeft': '1.2em'}),
            ], className="mb-2"),

            # html.Br(),

            html.Hr(style={
               'borderTopWidth': '3px',         # Grosor/Ancho de la línea: 3 píxeles
                'borderTopStyle': 'solid',      # Estilo de la línea: 'solid', 'dashed', 'dotted', 'double', etc.
                'borderTopColor': 'white',       # Color de la línea: 'white', '#FFFFFF', 'rgb(255,255,255)'
                'width': '100%',                  # Longitud: 80% del ancho del contenedor. Puede ser en px también (ej: '200px')
                # Para asegurar que solo el borde superior sea visible y no otros por defecto del navegador:
                'borderLeft': 'none',
                'borderRight': 'none',
                'borderBottom': 'none',
                # Opcional: para centrar la línea si su 'width' es menor al 100% y darle espacio vertical
                #'marginTop': '1rem',             # Margen superior (1rem es una unidad relativa al tamaño de fuente)
                #'marginBottom': '1rem',          # Margen inferior
                #'marginLeft': 'auto',            # Centra horizontalmente si width < 100%
                #'marginRight': 'auto'            # Centra horizontalmente si width < 100%
            }),  

            html.Br(),

            html.Div([
                html.H2("Key Technologies Used", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'color': 'white'}),
                dbc.ListGroup([
                    dbc.ListGroupItem([
                        html.Strong("Python:"), 
                            " Main programming language"
                    ], className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem([
                        html.Strong("Spark:"),
                         " For processing and scaling data"
                    ], className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem([
                        html.Strong("statsmodels:"),
                         " Python library for ARIMA"
                    ], className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem([
                        html.Strong("Google Cloud & BigQuery:"),
                         " Cloud platform"
                    ], className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'}),
                    dbc.ListGroupItem([
                        html.Strong("Dash:"),
                         " Python library for dashboards"
                    ], className="custom-list-item", style={'marginLeft': '2em', 'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'backgroundColor': 'transparent', 'border': 'none', 'padding': '0.2rem 0'})
                ],  flush=True)
            ], className="mb-2"),

             
             html.Div([
                html.H2("Data Source", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'color': 'white'}),
                html.P(
                    "Data was obtained from:",
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'marginLeft': '1.2em'}  # Indent
                ),
                html.A(
                    "E-Commerce Data: Online Retail II (Kaggle)",
                    href="https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci",
                    target="_blank",  # Opens link in a new tab
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': 'white', 'marginLeft': '1.2em'}
                ),
            ], className="mb-2"),


            html.Div([
                html.H3("GitHub Repository", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'color': 'white'}),
                html.P(
                    "Code and additional details are available on GitHub:",
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'marginLeft': '1.2em'}  # Indent
                ),
                html.A(
                    "GitHub",
                    href="https://github.com/mathematician18/Online-Retail-Sales-Forecasting",
                    target="_blank",
                    style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': 'white', 'marginLeft': '1.2em'}
                ),
            ], className="mb-2"),


            html.Div([
                html.H3("Explore the Analysis", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'color': 'white'}),
                html.P("Dive deeper into the analysis and visualizations:", style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'marginLeft': '1.2em'}),
                html.Div([
                    dbc.Button("Data Analysis", color="primary", href="/on_retail", className="mr-2", style={'marginRight': '10px', 'fontSize': '0.9rem'}),
                    dbc.Button("Forecasting", color="primary", href="/arima", style={'fontSize': '0.9rem'})
                ], className="d-flex"), # Use d-flex for horizontal button layout
            ], className="mt-3"),

            html.Div([
                html.H3("Contact Information", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'color': 'white', 'marginLeft': '65%', 'textAlign': 'left'}),
                html.P("Feel free to reach out!", style={'fontFamily': 'Arial', 'fontSize': '0.8rem', 'color': '#cccccc', 'marginLeft': '65%', 'textAlign': 'left'}),
                html.Div([
                    html.P("Gabriela Inzunza Gómez", style={'fontFamily': 'Arial', 'fontSize': '0.7rem', 'color': 'white', 'lineHeight': '0.5'}),
                    html.P(html.A("LinkedIn", href="https://linkedin.com/in/gabriela-inzunza-gomez", target="_blank", style={'fontFamily': 'Arial', 'fontSize': '0.7rem', 'color': 'white', 'lineHeight': '0.5'})),
                    html.P("g.inzunza.g@seintegra.pro", style={'fontFamily': 'Arial', 'fontSize': '0.7rem', 'color': 'white', 'lineHeight': '0.5'})
                ], style={'marginLeft': '65%', 'textAlign': 'left'}) # Push to the right
            ], className="mt-3")

        ], width=10, md=8, lg=8, style={'margin': '0 auto'})
    ]), #cierra dbc.row linea 30
], fluid=True, style={'backgroundColor': 'black', 'padding': '15px', 'borderRadius': '10px'}) 

