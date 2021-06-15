
# code for creating choropleth map of USA states
# import plotly library
import plotly
  
# import plotly.express module
# this module is used to create entire figures at once
import plotly.express as px
import json

with open("geojson.json") as file:
    be = json.load(file)

sources=[{"type": "FeatureCollection", 'features': [feat]} for feat in be['features']]
tx_ids=[be['features'][k]['properties']['Stadtteil'] for k in range(len(be['features']))]

# create figure
fig = px.choropleth(locationmode="geojson-id", color=[1], geojson=be, scope="europe")
  
fig.show()

https://medium.com/analytics-vidhya/create-geomaps-using-graph-objects-and-geojson-plotly-dcfb4067e3a6