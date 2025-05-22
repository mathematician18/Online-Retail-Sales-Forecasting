#!/usr/bin/env python
# coding: utf-8

# arima.py 

import dash
import argparse
import webbrowser
import threading
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import statsmodels.api as sm
import numpy as np
import os
import dash_bootstrap_components as dbc

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, sum as spark_sum
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from google.cloud import bigquery
from google.oauth2 import service_account
from dash import html, dcc, page_container, page_registry
from dash.dependencies import Input, Output, State # Se requiere State para el Modal

# Para pop-up refactorizado ARIMA_Highlights.py:
#from ARIMA_Highlights import get_arima_highlights_layout

# Configuración de argumentos
parser = argparse.ArgumentParser(description="Ejecuta el análisis ARIMA con Spark y BigQuery.")
parser.add_argument("--key_path", required=True, help="Ruta al archivo de credenciales de Google Cloud.")
parser.add_argument("--project_id", required=True, help="ID del proyecto de Google Cloud.")
args = parser.parse_args()

KEY_PATH = args.key_path
PROJECT_ID = args.project_id

# Dash app
dash.register_page(__name__, path="/arima", name="Forecasting")


# 🌟 Crear sesión de Spark (usando las variables de los argumentos)
spark = SparkSession.builder \
    .appName('BigQuery_Spark_OnlineRetail') \
    .config('spark.jars.packages', 'com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.32.2') \
    .config('credentialsFile', KEY_PATH) \
    .config('spark.hadoop.google.cloud.auth.service.account.enable', 'true') \
    .config('spark.hadoop.google.cloud.auth.service.account.json.keyfile', KEY_PATH) \
    .config('parentProject', PROJECT_ID) \
    .config('viewsEnabled', 'true') \
    .config('materializationDataset', 'temp_ds') \
    .getOrCreate()

print("✅ SparkSession creada exitosamente")

# Desactivar Arrow
spark.conf.set("spark.google.cloud.bigquery.arrow.enable", "false")
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "false")

# 📥 Leer tabla de BigQuery directamente
spark_df = spark.read.format('bigquery') \
    .option('table', 'online-retail-warehouse.online_retail_dw.transactions') \
    .option('credentialsFile', KEY_PATH) \
    .option('parentProject', PROJECT_ID) \
    .option("readDataFormat", "AVRO") \
    .load()

print(f"✅ Datos cargados de BigQuery: {spark_df.count()} filas")

# Preprocesamiento
spark_df = spark_df.withColumn("InvoiceDate", to_date(col("InvoiceDate")))
spark_df = spark_df.withColumn("Sales", col("Quantity") * col("Price"))
daily_sales = spark_df.groupBy("InvoiceDate").agg(spark_sum("Sales").alias("TotalSales")).limit(1000)

# Convertir a Pandas
pdf = daily_sales.toPandas().sort_values("InvoiceDate")
pdf["InvoiceDate"] = pd.to_datetime(pdf["InvoiceDate"])
pdf.set_index("InvoiceDate", inplace=True)

# Descomposición estacional
decomposition = sm.tsa.seasonal_decompose(pdf["TotalSales"], model='additive', period=30)

# Modelo ARIMA estacional
order = (1,1,1)
seasonal_order = (1,1,1,30)
model = sm.tsa.statespace.SARIMAX(pdf["TotalSales"], order=order, seasonal_order=seasonal_order)
results = model.fit(disp=False)


# Como NO se refactoriza ARIMA_Highlights.py su layout:
def get_arima_highlights_content_directly():
    return dbc.Container([ # O simplemente el contenido interno si el modal ya es un contenedor
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
    ], className="mb-2", fluid=True) # fluid=True para que el container se ajuste mejor al modal


# Layout de arima
layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='📈 ARIMA Forecasting', children=[
            html.P("Sales Forecast with ARIMA", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'marginLeft': '1.2em'}),
            dcc.Slider(id='forecast-days', min=10, max=180, step=10, value=60,
                       marks={i: str(i) for i in range(10, 181, 30)}),
            dcc.Graph(id='forecast-graph'),
            html.Pre(id='model-summary', style={'whiteSpace': 'pre-wrap', 'fontSize': 12}),
        
            html.Div([
                # Botón para abrir el Modal
                dbc.Button("Explore ARIMA Highlights", id="open-highlights-modal", color="info", className="mt-3 mb-3"),
                # Definición del Modal
                dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("ARIMA Model Highlights")),
                        dbc.ModalBody(
                            # Aquí va el contenido.
                            # Si se importa la función:
                            #get_arima_highlights_layout()
                            # Si se copia el contenido directamente:
                            get_arima_highlights_content_directly()
                        ),
                        dbc.ModalFooter(
                            dbc.Button("Cerrar", id="close-highlights-modal", className="ml-auto", color="secondary")
                        ),
                    ],
                    id="highlights-modal",
                    is_open=False,      # El modal está cerrado por defecto
                    size="lg",          # Tamaño del modal: "sm", "lg", "xl"
                    centered=True,      # Para centrar el modal verticalmente
                    scrollable=True,    # Si el contenido es largo
                ),
            ], style={'textAlign': 'right'}), # Alinea el botón a la derecha
        ]),
        dcc.Tab(label='📊 Seasonal Decomposition', children=[
            html.H1("Trend, Seasonality and Noise", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'marginLeft': '1.2em'}),
            dcc.Graph(id='trend', figure=px.line(x=decomposition.trend.index, y=decomposition.trend.values, labels={'x': 'Date', 'y': 'Trend'})),
            dcc.Graph(id='seasonal', figure=px.line(x=decomposition.seasonal.index, y=decomposition.seasonal.values, labels={'x': 'Date', 'y': 'Seasonality'})),
            dcc.Graph(id='resid', figure=px.line(x=decomposition.resid.index, y=decomposition.resid.values, labels={'x': 'Date', 'y': 'Residue'}))
        ]),
        dcc.Tab(label='📅 Historical Data', children=[
            html.H1("Historical Daily Sales", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'marginLeft': '1.2em'}),
            dcc.Graph(id='hist-data', figure=px.bar(pdf, x=pdf.index, y="TotalSales", title="Daily Sales"))
        ])
    ])
])

@dash.callback(
    Output('forecast-graph', 'figure'),
    Output('model-summary', 'children'),
    Input('forecast-days', 'value')
)
def update_forecast(n_days):
    forecast = results.get_forecast(steps=n_days)
    forecast_index = pd.date_range(pdf.index.max() + pd.Timedelta(days=1), periods=n_days)
    forecast_df = pd.DataFrame({
        "Date": forecast_index,
        "Prediction": forecast.predicted_mean,
        "Lower": forecast.conf_int().iloc[:, 0],
        "Upper": forecast.conf_int().iloc[:, 1]
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pdf.index, y=pdf["TotalSales"], name='Historical'))
    fig.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Prediction"], name='Prediction'))
    fig.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Lower"], name='Lower', line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Upper"], name='Upper', line=dict(dash='dot')))
    fig.update_layout(title="ARIMA Forecast with Confidence Intervals", xaxis_title="Date", yaxis_title="Sales")

    summary_text = str(results.summary())
    return fig, summary_text

    # Callback para abrir y cerrar el modal
@dash.callback(
    Output("highlights-modal", "is_open"),
    [Input("open-highlights-modal", "n_clicks"), Input("close-highlights-modal", "n_clicks")],
    [State("highlights-modal", "is_open")],
)
def toggle_modal(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

#abre el servidor
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")


# 🚀 Ejecutar servidor de Dash solo si el script se ejecuta directamente
#if __name__ == '__main__':
    # Para ejecutar Dash directamente sin argumentos:
    # KEY_PATH_LOCAL = r'C:\Users\ginzu\Documents\dataScience\Data warehousing\online-retail-warehouse-fd2f24b35fc6.json'
    # PROJECT_ID_LOCAL = "online-retail-warehouse"
    # spark_local = create_spark_session(KEY_PATH_LOCAL, PROJECT_ID_LOCAL) # Crear una sesión local si es necesario
    
#    threading.Timer(1.5, open_browser).start()
#    app.run(debug=True, port=8050)
#    # pass

