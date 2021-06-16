# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from os import name
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components.Div import Div
from dash_html_components.Span import Span
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from urllib.request import urlopen
import json

from plotly.subplots import make_subplots

external_stylesheets = [dbc.themes.BOOTSTRAP]

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

df = pd.read_csv("data/resulted_data/kmeans/CLUSTER_PROVINCES.csv")
df = df.rename(columns={"PROVINCE": "Provincie", "INFECTION_RATE": "Infectie graad", "HOSPITALISATION_RATE": "Hospitalisatie graad", "TEST_POS_PERCENTAGE": "Percentage positieve testen", "CLUSTER": "Cluster"})
df = df.astype({"Cluster": "int32"})
df = df.round(2)
with open('geojson.json') as file:
    be = json.load(file)

fig = px.choropleth(df, geojson=be, locations="Provincie", featureidkey="properties.NameDUT", projection="mercator", color="Cluster", hover_data=["Provincie", "Infectie graad", "Hospitalisatie graad", "Percentage positieve testen", "Cluster"])
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(dragmode=False, showlegend=False)

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

            html.Div({

            }, id='general-info-div'),

            html.Div([

            ], id='active-div'),

            html.Div([

            ], id='cases-div'),

            html.Div([

            ], id='recovered-div'),

            html.Div([

            ], id='deaths-div'),
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
            dcc.Graph(
                figure=fig,
                config={'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'zoomInGeo', 'zoomOutGeo']}
            )
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


##########################
###                    ###
### CALLBACKS FOR TABS ###
###                    ###
##########################


@app.callback(
    Output('general-info-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_general_info(province):
    df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
    df = df[ df['REGION'] == province ]

    if province == "Belgium":
        active_infections = df['ACTIVE_CASES'].iloc[-1]
        cumulative_cases = df['CUMULATIVE_CASES'].iloc[-1]
        cumulative_recovered = df['CUMULATIVE_RECOVERED'].iloc[-1]
        cumulative_deaths = df['CUMULATIVE_DEATHS'].iloc[-1]
        div = html.Div([
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader('Active cases'),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(active_infections, className='card-text')
                        ])
                    ], style={
                        "border-left": "5px solid CornflowerBlue",
                    }), 
                    width=2
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader('Total cases'),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(cumulative_cases, className='card-text')
                        ])
                    ], style={
                        "border-left": "5px solid orange",
                    }), 
                    width=2
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader('Total recovered'),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(cumulative_recovered, className='card-text')
                        ])
                    ], style={
                        "border-left": "5px solid green",
                    }), 
                    width=2
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader('Total Deaths'),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(cumulative_deaths, className='card-text')
                        ])
                    ], style={
                        "border-left": "5px solid red",
                    }), 
                    width=2
                ),
            ], className="justify-content-center m-0")
        ])
    else:
        active_infections = df["ACTIVE_CASES"].iloc[-1]
        cumulative_cases = df["CUMULATIVE_CASES"].iloc[-1]
        cumulative_recovered = df["CUMULATIVE_RECOVERED"].iloc[-1]

        div = html.Div([
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader('Active cases'),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(active_infections, className='card-text')
                        ])
                    ], style={
                        "border-left": "5px solid CornflowerBlue",
                    }), 
                    width=2
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader('Total cases'),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(cumulative_cases, className='card-text')
                        ])
                    ], style={
                        "border-left": "5px solid orange",
                    }), 
                    width=2
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader('Total recovered'),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(cumulative_recovered, className='card-text')
                        ])
                    ], style={
                        "border-left": "5px solid green",
                    }), 
                    width=2
                ),
            ], className="justify-content-center")
        ])

    return [div]


###############################
###                         ###
### CALLBACKS FOR CASES TAB ###
###                         ###
###############################


@app.callback(
    Output('active-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_active(province):
    df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
    df = df[ df["REGION"] == province ]

    # active_cases = px.line(x=df['DATE'], y=df['ACTIVE_CASES'], labels={'x': 'Datum', 'y': 'Actieve infecties'}, title='Actieve infecties')

    fig = make_subplots(
        rows=1,
        cols=1,
        subplot_titles=(
            'Actieve infecties',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['ACTIVE_CASES'],
            mode='lines',
            line=dict(color='CornflowerBlue'),
        ),
        row=1, col=1
    )

    fig.update_layout(hovermode="x unified")

    return [dcc.Graph(figure=fig)]

@app.callback(
    Output('cases-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_cases(province):
    df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
    df = df[ df["REGION"] == province ]

    # new_cases = px.line(x=df['DATE'], y=df['NEW_CASES'], labels={'x': 'Datum', 'y': 'Nieuwe infecties'})
    # cum_cases = px.line(x=df['DATE'], y=df['CUMULATIVE_CASES'], labels={'x': 'Datum', 'y': 'Cumulatieve infecties'})

    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'Nieuwe besmettingen per dag',
            'Cumulatief aantal besmettingen'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['NEW_CASES'],
            mode='lines',
            line=dict(color='orange'),
            name=""
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['CUMULATIVE_CASES'],
            mode='lines',
            line=dict(color='orange'),
            name=""
        ),
        row=1, col=2
    )

    fig.update_layout(hovermode="x unified", showlegend=False)

    return [dcc.Graph(figure=fig)]

@app.callback(
    Output('recovered-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_recovered(province):
    df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
    df = df[ df["REGION"] == province ]
    # new_recovered = px.line(x=df['DATE'], y=df['NEW_RECOVERED'], labels={'x': 'Datum', 'y': 'Nieuwe herstelden'})
    # cum_recovered = px.line(x=df['DATE'], y=df['CUMULATIVE_RECOVERED'], labels={'x': 'Datum', 'y': 'Cumulatief aantal herstelden'})
    
    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'Nieuwe recoveries per dag',
            'Cumulatief aantal recoveries'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['NEW_RECOVERED'],
            mode='lines',
            line=dict(color='green'),
            name=""
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['CUMULATIVE_RECOVERED'],
            mode='lines',
            line=dict(color='green'),
            name=""
        ),
        row=1, col=2
    )

    fig.update_layout(hovermode="x unified", showlegend=False)

    return [dcc.Graph(figure=fig)]

@app.callback(
    Output('deaths-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_deaths(province):
    if province == "Belgium":
        df = pd.read_csv(f'data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
        df = df[ df["REGION"] == province ]
        # new_deaths = px.line(x=df['DATE'], y=df['NEW_DEATHS'], labels={'x': 'Datum', 'y': 'Nieuwe doden'})
        # cum_deaths = px.line(x=df['DATE'], y=df['CUMULATIVE_DEATHS'], labels={'x': 'Datum', 'y': 'Cumulatief doden'})
        # return [dcc.Graph(figure=new_deaths), dcc.Graph(figure=cum_deaths)]

        fig = make_subplots(
            rows=1, 
            cols=2,
            subplot_titles=(
                'Nieuwe sterftegevallen per dag',
                'Cumulatief aantal doden'
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df['DATE'], 
                y=df['NEW_DEATHS'],
                mode='lines',
                line=dict(color='red'),
                name=""
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df['DATE'], 
                y=df['CUMULATIVE_DEATHS'],
                mode='lines',
                line=dict(color='red'),
                name=""
            ),
            row=1, col=2
        )

        fig.update_layout(hovermode="x unified", showlegend=False)

        return [dcc.Graph(figure=fig)]
    else:
        return []


#####################################
###                               ###
### CALLBACKS FOR PREDICTIONS TAB ###
###                               ###
#####################################


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


##########################################
###                                    ###
### CALLBACKS FOR HOSPITALISATIONS TAB ###
###                                    ###
##########################################


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


###############################
###                         ###
### CALLBACKS FOR TESTS TAB ###
###                         ###
###############################


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