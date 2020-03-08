import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output



df = pd.read_csv('Data-Viz-dataset-3.csv')

Lat = df["Lat"]
Lon = df["Lon"]
Num = df["Num of fights"]

mapbox_access_token = 'pk.eyJ1IjoidmluY2VudHJ5ayIsImEiOiJjazdmMXhyMm4wd2JhM2ZwcTJmdzgxdTU1In0.cgIhm37BjcdNsC97dNqSlA'

datamap = go.Data([go.Scattermapbox(
    lat = Lat,
    lon = Lon,
    text = df["Text"],
    mode = 'markers',
    line = dict(width = 2),
    marker = go.Marker(
        size = 11
      )
    )])

layoutmap = go.Layout(
    title='UFC Events',
    height = 700,
    autosize = True,
    showlegend = False,
    hovermode = 'closest',
    geo = dict(
        projection = dict(type = "equirectangular"),
        ),
    mapbox = dict(
        accesstoken = mapbox_access_token,
        bearing = 1,
        pitch = 0,
        zoom = 0,
        style = 'outdoors'
    ),
)

fig = dict( data=datamap, layout=layoutmap )


ufc_df=pd.read_csv('data.csv')

ufc_df.sort_values("R_fighter", inplace = True)
ufc_df.drop_duplicates(subset ="R_fighter",
                     keep = False, inplace = True)

ufc_df['year'] = ufc_df['date'].apply(lambda x : x.split('-')[0])

ufc_df_new = ufc_df[['R_fighter','R_Reach_cms','year','R_wins','R_win_by_Submission','R_Weight_lbs','R_longest_win_streak','R_losses']].copy()
ufc_news= ufc_df_new[ufc_df_new.R_wins!=0]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


features = ufc_news.columns

app.layout = html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis',
                options=[{'label': i.title(), 'value': i} for i in features],
                value='R_Weight_lbs'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': i.title(), 'value': i} for i in features],
                value='R_Reach_cms'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

        dcc.Graph(
            id='feature-graphic'),
        html.Div([
        html.P(html.Label('UFC Events around the World')),
        dcc.Graph(id='Mapevents', figure=fig)
    ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        html.P(html.Label('UFC Main event 2020')),
        html.Div([
        html.Img(id='Main Event ', src='https://raw.githubusercontent.com/OTB-X/OB.App/master/UFC%20209.jpeg', height= 400,style={'width': '48%', 'float': 'right', 'display': 'inline-block'} )])
    ],
            style={'padding':10}
)
@app.callback(
    Output('feature-graphic','figure'),
    [Input('xaxis', 'value'),
     Input('yaxis', 'value')])
def update_graph(xaxis_name, yaxis_name):
    return {
        'data': [go.Scatter(
            x=ufc_news[xaxis_name],
            y=ufc_news[yaxis_name],
            text=['R_wins'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={'title': xaxis_name.title()},
            yaxis={'title': yaxis_name.title()},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
