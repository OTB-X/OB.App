import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import dash 
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

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
                value='R_wins'
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
            id='feature-graphic')
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
