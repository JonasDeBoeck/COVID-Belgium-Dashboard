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
import dash_table
import dash_bootstrap_components as dbc
from geojson_rewind import rewind
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from urllib.request import urlopen
import json
from datetime import date

from plotly.subplots import make_subplots

external_stylesheets = [dbc.themes.BOOTSTRAP, "https://use.fontawesome.com/releases/v5.15.3/css/all.css"]

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

df["Cluster"] += 1
df = df.round(2)
with open('geojson.json', encoding="utf-8") as file:
    be = json.load(file)

be = rewind(be, rfc7946=False)

cluster_be = px.choropleth(df, geojson=be, locations="Provincie", featureidkey="properties.NameDUT", projection="mercator", color="Cluster", hover_data=["Provincie", "Infectie graad", "Hospitalisatie graad", "Percentage positieve testen", "Cluster"], height=800)

cluster_be.update_geos(fitbounds="locations", visible=False)
cluster_be.update_layout(dragmode=False, coloraxis_showscale=False)

cluster_metadata = pd.read_csv('data/resulted_data/kmeans/CLUSTER_METADATA.csv')
cluster_metadata = round(cluster_metadata, 2)

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
                clearable=False,
                style={
                    "width": "200px",
                    "margin": "auto",
                    "marginTop": "2rem"
                }
            ),

            html.Div([

            ], 
                id='general-info-div',
                style={
                    "marginTop": "2rem"
                }
            ),

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
                clearable=False,
                style={
                    "width": "200px",
                    "margin": "auto",
                    "marginTop": "2rem"
                }
            ),

            html.Div([

            ],
                id="predictions-info-div",
                style={
                    "marginTop": "2rem"
                }
            ),

            html.Div(
                id="predictions-div",
            ),
        ])
    elif tab == 'clustering':
        return html.Div([

            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=cluster_be,
                        config={'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'zoomInGeo', 'zoomOutGeo']}
                    ),
                ],
                    className="p-0"
                ),

                dbc.Col([
                    html.Div([
                        dash_table.DataTable(
                        id="cluster-info-table",
                        columns=[{"name": i, "id": i} for i in cluster_metadata.columns],
                        data=cluster_metadata.to_dict('records'),
                        style_cell={'textAlign': 'left'},
                        )
                    ]),
                ], 
                    className="d-flex align-items-center justify-content-center p-0"
                ),
            ],
                className="m-0"
            ),
        ],
            style={
                "marginTop": "2em"
            }
        )
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
                clearable=False,
                style={
                    "width": "200px",
                    "margin": "auto",
                    "marginTop": "2rem"
                }
            ),

            html.Div([

            ],
                id="hospitalisations-info-div",
                style={
                    "marginTop": "2rem"
                }
            ),

            html.Div(
                id="hospitalisations-div"
            ),
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
                clearable=False,
                style={
                    "width": "200px",
                    "margin": "auto",
                    "marginTop": "2rem"
                }
            ),

            html.Div([

            ],
                id="tests-info-div",
                style={
                    "marginTop": "2rem"
                }
            ),

            html.Div(
                id="tests-div"
            ),
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
                        dbc.CardHeader([
                            html.P(
                                ['Active cases'],
                                style={
                                    "marginBottom": "0"
                                }
                            ),
                            html.I(
                                className="fas fa-head-side-cough",
                                style={
                                    "fontSize": "2rem",
                                    "color": "CornflowerBlue"
                                }
                            )
                        ], style={
                            "display": "flex",
                            "flexDirection": "row",
                            "justifyContent": "space-between",
                            "alignItems": "center"
                        }),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(active_infections, className='card-text')
                        ])
                    ], style={
                        "borderLeft": "5px solid CornflowerBlue",
                    }), 
                    width=2
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader([
                            html.P(
                                ['Total cases'],
                                style={
                                    "marginBottom": "0"
                                }
                            ),
                            html.I(
                                className="fas fa-viruses",
                                style={
                                    "fontSize": "2rem",
                                    "color": "orange"
                                }
                            )
                        ], style={
                            "display": "flex",
                            "flexDirection": "row",
                            "justifyContent": "space-between",
                            "alignItems": "center"
                        }),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(cumulative_cases, className='card-text')
                        ])
                    ], style={
                        "borderLeft": "5px solid orange",
                    }), 
                    width=2
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader([
                            html.P(
                                ['Total recovered'],
                                style={
                                    "marginBottom": "0"
                                }
                            ),
                            html.I(
                                className="fas fa-virus-slash",
                                style={
                                    "fontSize": "2rem",
                                    "color": "green"
                                }
                            )
                        ], style={
                            "display": "flex",
                            "flexDirection": "row",
                            "justifyContent": "space-between",
                            "alignItems": "center"
                        }),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(cumulative_recovered, className='card-text')
                        ])
                    ], style={
                        "borderLeft": "5px solid green",
                    }), 
                    width=2
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader([
                            html.P(
                                ['Total deaths'],
                                style={
                                    "marginBottom": "0"
                                }
                            ),
                            html.I(
                                className="fas fa-cross",
                                style={
                                    "fontSize": "2rem",
                                    "color": "red"
                                }
                            )
                        ], style={
                            "display": "flex",
                            "flexDirection": "row",
                            "justifyContent": "space-between",
                            "alignItems": "center"
                        }),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(cumulative_deaths, className='card-text')
                        ])
                    ], style={
                        "borderLeft": "5px solid red",
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
                        dbc.CardHeader([
                            html.P(
                                ['Active cases'],
                                style={
                                    "marginBottom": "0"
                                }
                            ),
                            html.I(
                                className="fas fa-head-side-cough",
                                style={
                                    "fontSize": "2rem",
                                    "color": "CornflowerBlue"
                                }
                            )
                        ], style={
                            "display": "flex",
                            "flexDirection": "row",
                            "justifyContent": "space-between",
                            "alignItems": "center"
                        }),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(active_infections, className='card-text')
                        ])
                    ], style={
                        "borderLeft": "5px solid CornflowerBlue",
                    }), 
                    width=2
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader([
                            html.P(
                                ['Total cases'],
                                style={
                                    "marginBottom": "0"
                                }
                            ),
                            html.I(
                                className="fas fa-viruses",
                                style={
                                    "fontSize": "2rem",
                                    "color": "orange"
                                }
                            )
                        ], style={
                            "display": "flex",
                            "flexDirection": "row",
                            "justifyContent": "space-between",
                            "alignItems": "center"
                        }),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(cumulative_cases, className='card-text')
                        ])
                    ], style={
                        "borderLeft": "5px solid orange",
                    }), 
                    width=2
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader([
                            html.P(
                                ['Total recovered'],
                                style={
                                    "marginBottom": "0"
                                }
                            ),
                            html.I(
                                className="fas fa-virus-slash",
                                style={
                                    "fontSize": "2rem",
                                    "color": "green"
                                }
                            )
                        ], style={
                            "display": "flex",
                            "flexDirection": "row",
                            "justifyContent": "space-between",
                            "alignItems": "center"
                        }),
                        dbc.CardBody([
                            html.H5(f'{province}', className='card-title'),
                            html.P(cumulative_recovered, className='card-text')
                        ])
                    ], style={
                        "borderLeft": "5px solid green",
                    }), 
                    width=2
                ),
            ], className="justify-content-center m-0")
        ])

    return [div]

@app.callback(
    Output('predictions-info-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_predictions_info(province):
    df = pd.read_csv(f'data/resulted_data/neural_network/{province}/pred_all.csv')
    df["Data"] = pd.to_datetime(df["Data"]).dt.date
    days_trained = df[ df['Used in Train'] == True]
    days_trained = len(days_trained)
    days_predicted = df[ df['Used in Train'] == False]
    days_predicted = len(days_predicted)
    Rt = round(df[df['Data'] == date.today()]['Rt'], 2)

    div = html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Days trained'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-dumbbell",
                            style={
                                "fontSize": "2rem",
                                "color": "CornflowerBlue"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{province}', className='card-title'),
                        html.P(days_trained, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid CornflowerBlue",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Days predicted'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-chart-line",
                            style={
                                "fontSize": "2rem",
                                "color": "orange"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{province}', className='card-title'),
                        html.P(days_predicted, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid orange",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Reproduction factor'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-people-arrows",
                            style={
                                "fontSize": "2rem",
                                "color": "crimson"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{province}', className='card-title'),
                        html.P(Rt, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid crimson",
                }), 
                width=2
            ),
        ], className="justify-content-center m-0")
    ])

    return [div]

@app.callback(
    Output('hospitalisations-info-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_hospitalisations_info(province):
    df = pd.read_csv(f'data/filtered_data/HOSP.csv')
    df = df[ df['REGION'] == province ]

    total_in_icu = df['TOTAL_IN_ICU'].iloc[-1]
    new_in = df['NEW_IN'].iloc[-1]
    total_hospitalisations = df["NEW_IN"].sum()

    div = html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Total in ICU'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-procedures",
                            style={
                                "fontSize": "2rem",
                                "color": "CornflowerBlue"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{province}', className='card-title'),
                        html.P(total_in_icu, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid CornflowerBlue",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['New Hospitalisations'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-hospital-user",
                            style={
                                "fontSize": "2rem",
                                "color": "green"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{province}', className='card-title'),
                        html.P(new_in, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid green",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Total Hospitalisations'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-hospital-user",
                            style={
                                "fontSize": "2rem",
                                "color": "darkseagreen"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{province}', className='card-title'),
                        html.P(total_hospitalisations, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid darkseagreen",
                }), 
                width=2
            ),
        ], className="justify-content-center m-0")
    ])

    return [div]

@app.callback(
    Output('tests-info-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_tests_info(province):
    df = pd.read_csv(f'data/filtered_data/TESTS.csv')
    df = df[ df['REGION'] == province ]

    total_tests = df['TESTS_ALL'].sum()
    total_positive_tests = df['TESTS_ALL_POS'].sum()
    new_tests = df['TESTS_ALL'].iloc[-1]
    new_positive = df['TESTS_ALL_POS'].iloc[-1]

    div = html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['New tests'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-vials",
                            style={
                                "fontSize": "2rem",
                                "color": "CornflowerBlue"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{province}', className='card-title'),
                        html.P(total_tests, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid CornflowerBlue",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Total tests'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-vials",
                            style={
                                "fontSize": "2rem",
                                "color": "DarkCyan"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{province}', className='card-title'),
                        html.P(total_tests, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid DarkCyan",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['New positive tests'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-plus",
                            style={
                                "fontSize": "2rem",
                                "color": "green"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{province}', className='card-title'),
                        html.P(total_positive_tests, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid green",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Total positive tests'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-plus",
                            style={
                                "fontSize": "2rem",
                                "color": "darkseagreen"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{province}', className='card-title'),
                        html.P(total_positive_tests, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid darkseagreen",
                }), 
                width=2
            ),
        ], className="justify-content-center m-0")
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
    Output('predictions-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_predictions(province):
    df = pd.read_csv(f'data/resulted_data/neural_network/{province}/pred_all.csv')
    df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%Y-%m-%d')
    fig1 = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            'Actieve infecties',
            'Aantal recovered',
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=df['Data'], 
            y=df['Infected'],
            mode='lines',
            line=dict(color='CornflowerBlue'),
            name=""
        ),
        row=1, col=1
    )

    fig1.add_trace(
        go.Scatter(
            x=df['Data'], 
            y=df['Recovered'],
            mode='lines',
            line=dict(color='Green'),
            name=""
        ),
        row=1, col=2
    )

    fig2 = make_subplots(
        rows=1,
        cols=1,
        subplot_titles=(
            'Reproductie cijfer',
        )
    )

    fig2.add_trace(
        go.Scatter(
            x=df['Data'], 
            y=df['Rt'],
            mode='lines',
            line=dict(color='Crimson'),
        ),
        row=1, col=1
    )

    fig1.update_layout(hovermode='x unified', showlegend=False)
    fig2.update_layout(hovermode='x unified')

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]


##########################################
###                                    ###
### CALLBACKS FOR HOSPITALISATIONS TAB ###
###                                    ###
##########################################


@app.callback(
    Output('hospitalisations-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_hospitalisations(province):
    df = pd.read_csv(f'data/filtered_data/HOSP.csv')
    df = df[ df["REGION"] == province ]

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            'Mensen in ICU',
            'Aantal nieuwe opnames',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['TOTAL_IN_ICU'],
            mode='lines',
            line=dict(color='CornflowerBlue'),
            name=""
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['NEW_IN'],
            mode='lines',
            line=dict(color='Green'),
            name=""
        ),
        row=1, col=2
    )

    fig.update_layout(hovermode='x unified', showlegend=False)

    return [dcc.Graph(figure=fig)]


###############################
###                         ###
### CALLBACKS FOR TESTS TAB ###
###                         ###
###############################


@app.callback(
    Output('tests-div', 'children'),
    Input('predictions-province', 'value')
)
def update_province_tests(province):
    df = pd.read_csv(f'data/filtered_data/TESTS.csv')
    df = df[ df["REGION"] == province ]

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            'Aantal afgenomen testen',
            'Aantal positieve testen',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['TESTS_ALL'],
            mode='lines',
            line=dict(color='CornflowerBlue'),
            name=""
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['TESTS_ALL_POS'],
            mode='lines',
            line=dict(color='Green'),
            name=""
        ),
        row=1, col=2
    )

    fig.update_layout(hovermode='x unified', showlegend=False)

    return [dcc.Graph(figure=fig)]

if __name__ == '__main__':
    app.run_server(debug=True)