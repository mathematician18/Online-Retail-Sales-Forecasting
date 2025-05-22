# -*- coding: utf-8 -*-

import dash
import argparse
import os
import webbrowser
import threading
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import statsmodels.api as sm
import numpy as np
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, to_date, sum as spark_sum, avg as spark_avg, count as spark_count,
    date_format, month, year, hour, dayofweek, when, lit, to_date, lpad, concat_ws, countDistinct, avg, when # Añadir funciones necesarias
)
from pyspark.sql.window import Window
from pyspark.sql.types import TimestampType # Para conversiones si es necesario
from dash import Dash, dcc, html, Input, Output


# Configura tus rutas y credenciales
KEY_PATH = r'C:\Users\ginzu\Documents\dataScience\Data warehousing\online-retail-warehouse-fd2f24b35fc6.json'
PROJECT_ID = "online-retail-warehouse"

dash.register_page(__name__, path="/on_retail", name="Data Analysis")


# 1. SparkSession y carga de datos
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

spark.conf.set("spark.google.cloud.bigquery.arrow.enable", "false")
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "false")

spark_df = spark.read.format('bigquery') \
    .option('table', 'online-retail-warehouse.online_retail_dw.transactions') \
    .option('credentialsFile', KEY_PATH) \
    .option('parentProject', PROJECT_ID) \
    .option("readDataFormat", "AVRO") \
    .load()

# 2. Transformaciones necesarias
spark_df = spark_df.withColumn("InvoiceTimestamp", col("InvoiceDate").cast(TimestampType()))
spark_df = spark_df.withColumn("Hour", hour(col("InvoiceTimestamp")))
spark_df = spark_df.withColumn("DayOfWeekName", date_format(col("InvoiceTimestamp"), "EEEE"))
spark_df = spark_df.withColumn("Year", year(col("InvoiceTimestamp")))
spark_df = spark_df.withColumn("Month", month(col("InvoiceTimestamp")))
spark_df = spark_df.withColumn("Revenue", col("Quantity") * col("Price"))
spark_df = spark_df.withColumn("InvoiceDate", to_date(col("InvoiceTimestamp")))
spark_df = spark_df.filter(col("Customer_ID").isNotNull()) \
    .filter(~col("Invoice").cast("string").startswith("C")) \
    .withColumn("Customer_ID", col("Customer_ID").cast("string"))

# Listas para dropdowns
paises = ['all'] + sorted([row['Country'] for row in spark_df.select('Country').distinct().collect()])
meses = ['all'] + sorted([str(row['Month']) for row in spark_df.select('Month').distinct().collect()])
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# 3. Dash App
#app = Dash(__name__)
#app.title = "Online Retail Dashboard"


layout = html.Div([
    html.P("Online Retail Data Dashboard",
                #    className="lead text-center",
                    style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'marginLeft': '1.2em'}
                ),
    #html.H1("Online Retail Data Dashboard", style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='KPIs by Country', children=[
            html.Br(),
            dcc.Dropdown(id='kpi-country', options=[{'label': p, 'value': p} for p in paises], value='all'),
            html.Div(id='kpi-output')
        ]),
        dcc.Tab(label='Top Products by Income', children=[
            html.Br(),
            dcc.Dropdown(id='top-country', options=[{'label': p, 'value': p} for p in paises], value='all'),
            dcc.Slider(id='top-n', min=1, max=25, value=10, marks={i: str(i) for i in range(0, 25, 5)}),
            dcc.Graph(id='top-products-graph')
        ]),
        dcc.Tab(label='Monthly Income Evolution', children=[
            html.Br(),
            dcc.Dropdown(id='trend-country', options=[{'label': p, 'value': p} for p in paises], value='all'),
            dcc.Graph(id='monthly-trend-graph')
        ]),
        dcc.Tab(label='Heat Map Day vs Time', children=[
            html.Br(),
            dcc.Dropdown(id='heatmap-country', options=[{'label': p, 'value': p} for p in paises], value='all'),
            dcc.Dropdown(id='heatmap-month', options=[{'label': m, 'value': m} for m in meses], value='all'),
            dcc.Graph(id='heatmap-graph')
        ])
    ])
])

# 4. Callbacks Dash

# KPIs por país
@dash.callback(
    Output('kpi-output', 'children'),
    Input('kpi-country', 'value')
)
def update_kpis(country):
    df = spark_df if country == 'all' else spark_df.filter(col('Country') == country)
    agg = df.agg(
        spark_sum('Revenue').alias('TotalRevenue'),
        countDistinct('Customer_ID').alias('UniqueCustomers')
    ).collect()[0]
    invoice_revenue_df = df.groupBy('Invoice').agg(spark_sum('Revenue').alias('InvoiceRevenue'))
    avg_order = invoice_revenue_df.select(avg('InvoiceRevenue')).collect()[0][0]
    return html.Div([
        html.P(f"📍 Country: {country}", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'marginLeft': '1.2em'}),
        html.P(f"💰 Total revenues: ${agg['TotalRevenue']:,.2f}", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'marginLeft': '1.2em'}),
        html.P(f"👤 Unique clients: {agg['UniqueCustomers']}", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'marginLeft': '1.2em'}),
        html.P(f"🧾 Average by order: ${avg_order:,.2f}", style={'fontFamily': 'Arial', 'fontSize': '1.0rem', 'marginLeft': '1.2em'})
    ])

# Top productos por ingresos
@dash.callback(
    Output('top-products-graph', 'figure'),
    [Input('top-country', 'value'), Input('top-n', 'value')]
)
def update_top_products(country, n):
    df = spark_df if country == 'all' else spark_df.filter(col('Country') == country)
    product_sales_pd = df.groupBy("Description") \
        .agg(spark_sum("Revenue").alias("TotalRevenue")) \
        .orderBy(col("TotalRevenue").desc()) \
        .limit(n) \
        .toPandas()
    fig = px.bar(
        product_sales_pd,
        x='TotalRevenue',
        y='Description',
        orientation='h',
        title=f'🏆 Top {n} Products by Income'
    )
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=500 + (n * 20)
    )
    return fig

# Evolución mensual de ingresos
@dash.callback(
    Output('monthly-trend-graph', 'figure'),
    Input('trend-country', 'value')
)
def update_monthly_trend(country):
    df = spark_df if country == 'all' else spark_df.filter(col('Country') == country)
    df = df.filter(col('Year').isNotNull() & col('Month').isNotNull())
    ventas_mensuales = df.groupBy('Year', 'Month') \
        .agg(spark_sum('Revenue').alias('TotalRevenue')) \
        .orderBy('Year', 'Month')
    ventas_mensuales = ventas_mensuales.withColumn(
        'YearMonthStr',
        concat_ws('-', col('Year').cast('string'), lpad(col('Month').cast('string'), 2, '0'))
    )
    df_pandas = ventas_mensuales.select('YearMonthStr', 'TotalRevenue').toPandas()
    df_pandas = df_pandas[df_pandas['YearMonthStr'].notnull() & (df_pandas['YearMonthStr'] != '')]
    df_pandas['YearMonthDate'] = pd.to_datetime(df_pandas['YearMonthStr'].astype(str) + '-01', errors='coerce')
    df_pandas = df_pandas[df_pandas['YearMonthDate'].notnull()]
    df_pandas = df_pandas.sort_values('YearMonthDate', ascending=True)
    fig = px.line(
        df_pandas,
        x='YearMonthDate',
        y='TotalRevenue',
        title=f'🌍 Monthly Income Evolution - {country}',
        markers=True
    )
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Total Income (USD)',
        xaxis_tickformat='%Y-%m',
        hovermode='x unified',
        height=500
    )
    return fig

# Mapa de calor día vs hora
@dash.callback(
    Output('heatmap-graph', 'figure'),
    [Input('heatmap-country', 'value'), Input('heatmap-month', 'value')]
)
def update_heatmap(country, month):
    df = spark_df
    if country != 'all':
        df = df.filter(col('Country') == country)
    if month != 'all':
        df = df.filter(col('Month') == int(month))
    heatmap_data_spark = df.groupBy(
        date_format(col("InvoiceTimestamp"), "EEEE").alias("DayOfWeek"),
        hour(col("InvoiceTimestamp")).alias("Hour")
    ).agg(
        spark_sum("Revenue").alias("TotalRevenue")
    )
    heatmap_data_spark = heatmap_data_spark.withColumn(
        "DayOfWeekOrder",
        when(col("DayOfWeek") == "Monday", 1)
        .when(col("DayOfWeek") == "Tuesday", 2)
        .when(col("DayOfWeek") == "Wednesday", 3)
        .when(col("DayOfWeek") == "Thursday", 4)
        .when(col("DayOfWeek") == "Friday", 5)
        .when(col("DayOfWeek") == "Saturday", 6)
        .when(col("DayOfWeek") == "Sunday", 7)
    )
    heatmap_data_spark = heatmap_data_spark.orderBy("DayOfWeekOrder", "Hour")
    heatmap_data_pd = heatmap_data_spark.select("DayOfWeek", "Hour", "TotalRevenue").toPandas()
    heatmap_matrix = heatmap_data_pd.pivot(index="DayOfWeek", columns="Hour", values="TotalRevenue")
    heatmap_matrix = heatmap_matrix.reindex(days_order)
    fig = px.imshow(
        heatmap_matrix,
        labels=dict(x="Time of day", y="Day of Week", color="Income"),
        x=heatmap_matrix.columns,
        y=heatmap_matrix.index,
        color_continuous_scale="Viridis",
        aspect="auto"
    )
    titulo_mes = f"Mes: {month}" if month != 'all' else "Every month"
    titulo_pais = f"País: {country}" if country != 'all' else "All countries"
    fig.update_layout(title=f"Heat Map of Revenue by Day and Hour - {titulo_pais} - {titulo_mes}")
    return fig

# Para abrir servidor
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")



#if __name__ == '__main__':
#    threading.Timer(1.5, open_browser).start()
#    app.run(debug=True)
#    #pass