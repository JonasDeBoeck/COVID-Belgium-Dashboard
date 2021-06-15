# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from urllib.request import urlopen
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='cases', children=[
        dcc.Tab(label='Cases', value='cases'),
        dcc.Tab(label='Predictions', value='predictions'),
        dcc.Tab(label='Clustering', value='clustering'),
        dcc.Tab(label='Hospitalisations', value='hospitalisations'),
        dcc.Tab(label='Tests', value='tests'),
    ]),
    html.Div(id='tabs-content')
])

df = pd.read_csv('data/filtered_data/kmeans.csv')

with urlopen('https://raw.githubusercontent.com/mathiasleroy/Belgium-Geographic-Data/master/dist/polygons/geojson/Belgium.provinces.WGS84.geojson') as response:
    belgium = json.load(response)

cluster_map = px.choropleth(geojson=belgium)

@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'cases':
        return html.Div([
            dcc.Dropdown(
                id='predictions-province',
                options=[
                    {'label': 'Belgium', 'value': 'Belgium'},
                    {'label': 'Antwerpen', 'value': 'Antwerpen'},
                    {'label': 'Waals-Brabant', 'value': 'BrabantWallon'},
                    {'label': 'Brussel', 'value': 'Brussels'},
                    {'label': 'Henegouwen', 'value': 'Hainaut'},
                    {'label': 'Luik', 'value': 'Liège'},
                    {'label': 'Limburg', 'value': 'Limburg'},
                    {'label': 'Luxemburg', 'value': 'Luxemburg'},
                    {'label': 'Namen', 'value': 'Namur'},
                    {'label': 'Oost-Vlaanderen', 'value': 'OostVlaanderen'},
                    {'label': 'Vlaams-Brabant', 'value': 'VlaamsBrabant'},
                    {'label': 'West-Vlaanderen', 'value': 'WestVlaanderen'},
                ],
                value='Belgium',
                clearable=False
            ),

            dcc.Graph(id='active-cases-graph'),

            dcc.Graph(id='new-cases-graph'),

            dcc.Graph(id='cumulative-cases-graph'),

            dcc.Graph(id='new-recovered-graph'),

            dcc.Graph(id='cumulative-recovered-graph'),

            dcc.Graph(id='new-deaths-graph'),

            dcc.Graph(id='cumulative-deaths-graph'),
        ])
    elif tab == 'predictions':
        return html.Div([
            dcc.Dropdown(
                id='predictions-province',
                options=[
                    {'label': 'Belgium', 'value': 'Belgium'},
                    {'label': 'Antwerpen', 'value': 'Antwerpen'},
                    {'label': 'Waals-Brabant', 'value': 'BrabantWallon'},
                    {'label': 'Brussel', 'value': 'Brussels'},
                    {'label': 'Henegouwen', 'value': 'Hainaut'},
                    {'label': 'Luik', 'value': 'Liège'},
                    {'label': 'Limburg', 'value': 'Limburg'},
                    {'label': 'Luxemburg', 'value': 'Luxemburg'},
                    {'label': 'Namen', 'value': 'Namur'},
                    {'label': 'Oost-Vlaanderen', 'value': 'OostVlaanderen'},
                    {'label': 'Vlaams-Brabant', 'value': 'VlaamsBrabant'},
                    {'label': 'West-Vlaanderen', 'value': 'WestVlaanderen'},
                ],
                value='Belgium',
                clearable=False
            ),

            dcc.Graph(id='cases-predictions-graph'),

            dcc.Graph(id='recoveries-predictions-graph'),

            dcc.Graph(id='rt-predictions-graph'),
        ])
    elif tab == 'clustering':
        return html.Div([
            dcc.Graph(figure=cluster_map)
        ])
    elif tab == 'hospitalisations':
        return html.Div([
            dcc.Dropdown(
                id='predictions-province',
                options=[
                    {'label': 'Belgium', 'value': 'Belgium'},
                    {'label': 'Antwerpen', 'value': 'Antwerpen'},
                    {'label': 'Waals-Brabant', 'value': 'BrabantWallon'},
                    {'label': 'Brussel', 'value': 'Brussels'},
                    {'label': 'Henegouwen', 'value': 'Hainaut'},
                    {'label': 'Luik', 'value': 'Liège'},
                    {'label': 'Limburg', 'value': 'Limburg'},
                    {'label': 'Luxemburg', 'value': 'Luxemburg'},
                    {'label': 'Namen', 'value': 'Namur'},
                    {'label': 'Oost-Vlaanderen', 'value': 'OostVlaanderen'},
                    {'label': 'Vlaams-Brabant', 'value': 'VlaamsBrabant'},
                    {'label': 'West-Vlaanderen', 'value': 'WestVlaanderen'},
                ],
                value='Belgium',
                clearable=False
            ),

            dcc.Graph(id='total-in-icu-graph'),

            dcc.Graph(id='hospitalisations-graph'),
        ])
    elif tab == 'tests':
        return html.Div([
            dcc.Dropdown(
                id='predictions-province',
                options=[
                    {'label': 'Belgium', 'value': 'Belgium'},
                    {'label': 'Antwerpen', 'value': 'Antwerpen'},
                    {'label': 'Waals-Brabant', 'value': 'BrabantWallon'},
                    {'label': 'Brussel', 'value': 'Brussels'},
                    {'label': 'Henegouwen', 'value': 'Hainaut'},
                    {'label': 'Luik', 'value': 'Liège'},
                    {'label': 'Limburg', 'value': 'Limburg'},
                    {'label': 'Luxemburg', 'value': 'Luxemburg'},
                    {'label': 'Namen', 'value': 'Namur'},
                    {'label': 'Oost-Vlaanderen', 'value': 'OostVlaanderen'},
                    {'label': 'Vlaams-Brabant', 'value': 'VlaamsBrabant'},
                    {'label': 'West-Vlaanderen', 'value': 'WestVlaanderen'},
                ],
                value='Belgium',
                clearable=False
            ),

            dcc.Graph(id='total-tests-graph'),

            dcc.Graph(id='total-pos-tests-graph'),
        ])

@app.callback(
    Output('cases-predictions-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_cases_predictions(province):
    df = pd.read_csv(f'data/resulted_data/neural_network/{province}/pred_all.csv')
    fig = px.line(x=df['Data'], y=df['Infected'], labels={'x': 'Datum', 'y': 'Actieve infecties'})
    return fig

@app.callback(
    Output('recoveries-predictions-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_recovered_predictions(province):
    df = pd.read_csv(f'data/resulted_data/neural_network/{province}/pred_all.csv')
    fig = px.line(x=df['Data'], y=df['Recovered'], labels={'x': 'Datum', 'y': 'Cumulatief aantal herstelden'})
    return fig

@app.callback(
    Output('rt-predictions-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_rt_predictions(province):
    df = pd.read_csv(f'data/resulted_data/neural_network/{province}/pred_all.csv')
    fig = px.line(x=df['Data'], y=df['Rt'], labels={'x': 'Datum', 'y': 'Reproductie factor'})
    return fig

@app.callback(
    Output('active-cases-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_active_cases(province):
    df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
    df = df[ df["REGION"] == province ]
    fig = px.line(x=df['DATE'], y=df['ACTIVE_CASES'], labels={'x': 'Datum', 'y': 'Actieve infecties'})
    return fig

@app.callback(
    Output('new-cases-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_new_cases(province):
    df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
    df = df[ df["REGION"] == province ]
    fig = px.line(x=df['DATE'], y=df['NEW_CASES'], labels={'x': 'Datum', 'y': 'Nieuwe infecties'})
    return fig

@app.callback(
    Output('cumulative-cases-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_cum_cases(province):
    df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
    df = df[ df["REGION"] == province ]
    fig = px.line(x=df['DATE'], y=df['CUMULATIVE_CASES'], labels={'x': 'Datum', 'y': 'Cumulatieve infecties'})
    return fig

@app.callback(
    Output('new-recovered-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_new_recoveries(province):
    df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
    df = df[ df["REGION"] == province ]
    fig = px.line(x=df['DATE'], y=df['NEW_RECOVERED'], labels={'x': 'Datum', 'y': 'Nieuwe herstelden'})
    return fig

@app.callback(
    Output('cumulative-recovered-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_cum_recoveries(province):
    df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
    df = df[ df["REGION"] == province ]
    fig = px.line(x=df['DATE'], y=df['CUMULATIVE_RECOVERED'], labels={'x': 'Datum', 'y': 'Cumulatief aantal herstelden'})
    return fig

@app.callback(
    Output('new-deaths-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_new_deaths(province):
    if province == "Belgium":
        df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
        df = df[ df["REGION"] == province ]
        fig = px.line(x=df['DATE'], y=df['NEW_DEATHS'], labels={'x': 'Datum', 'y': 'Nieuwe doden'})
        return fig
    else:
        return {}

@app.callback(
    Output('cumulative-deaths-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_cum_deaths(province):
    if province == "Belgium":
        df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
        df = df[ df["REGION"] == province ]
        fig = px.line(x=df['DATE'], y=df['CUMULATIVE_DEATHS'], labels={'x': 'Datum', 'y': 'Cumulatief doden'})
        return fig
    else:
        return {}

@app.callback(
    Output('total-in-icu-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_icu(province):
    df = pd.read_csv(f'data/filtered_data/HOSP.csv')
    df = df[ df["REGION"] == province ]
    fig = px.line(x=df['DATE'], y=df['TOTAL_IN_ICU'], labels={'x': 'Datum', 'y': 'Totale intensive care'})
    return fig

@app.callback(
    Output('hospitalisations-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_icu(province):
    df = pd.read_csv(f'data/filtered_data/HOSP.csv')
    df = df[ df["REGION"] == province ]
    fig = px.line(x=df['DATE'], y=df['NEW_IN'], labels={'x': 'Datum', 'y': 'Nieuwe opnames'})
    return fig

@app.callback(
    Output('total-tests-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_total_tests(province):
    df = pd.read_csv(f'data/filtered_data/TESTS.csv')
    df = df[ df["REGION"] == province ]
    fig = px.line(x=df['DATE'], y=df['TESTS_ALL'], labels={'x': 'Datum', 'y': 'Aantal testen'})
    return fig

@app.callback(
    Output('total-pos-tests-graph', 'figure'),
    Input('predictions-province', 'value')
)
def update_province_total_tests(province):
    df = pd.read_csv(f'data/filtered_data/TESTS.csv')
    df = df[ df["REGION"] == province ]
    fig = px.line(x=df['DATE'], y=df['TESTS_ALL_POS'], labels={'x': 'Datum', 'y': 'Aantal positieve testen'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)