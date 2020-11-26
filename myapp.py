import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from datetime import datetime

data=pd.read_csv('full_grouped.csv')

df1=data.groupby('WHO Region')[['Confirmed', 'WHO Region']].sum().sort_values('Confirmed', 
                            ascending=False)[:15]

df_euro = data.loc[data['WHO Region'] == 'Europe']
df_sort_date = df_euro.sort_values('Date', ascending = True)

df3 = df_sort_date.set_index('Date')
df4 = df_sort_date.set_index('Country/Region')
df2 = df_sort_date.groupby('Date')[['Deaths', 'Recovered']].sum()

options = []


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = dash.Dash()

app.layout = html.Div([
    html.H1('Covid 19 Dashboard in Europe'),
    html.Div([html.H3('Enter country name:', style={'paddingRight':'30px'}),
    dcc.Dropdown(
          id ='Country',
        options = [{'label': i.title(), 'value': i} for i in df4.index], 
        value=['Malta'],
        multi=True
    )],style={'display':'inline-block', 'verticalAlign':'top'}),
    html.Div([html.H3('Select a start and end date:'),
              dcc.DatePickerRange(id='my_date_picker',
                                    min_date_allowed=datetime(2020,1,22),
                                    max_date_allowed=datetime(2020,7,28),
                                    start_date = datetime(2020,2,1),
                                    end_date =datetime(2020,7,28)
                                 )
             ],style={'display':'inline-block'}),  
    html.Div([
            html.Button(id='submit-button',
                        n_clicks=0,
                        children='Submit',
                        style={'fontSize':24, 'marginLeft':'30px'}
            )
    ],style={'display':'inline-block'}),
    
    dcc.Graph(id='my_graph',figure={
            'data': [
                {'x': df3.index, 'y': df3['New cases']}
            ], 
            }, 

    ), dcc.Graph(id='region cases',
                       figure={'data':
                               [{'x': df1.index,'y': df1['Confirmed'], 'type':'bar'}],

            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                       },
                'hovermode':'closest',
                
                'yaxis': {
       'title': 'Confirmed Cases'
            },                
                'title': 'Confirmed cases by Region'
        }
    },style={'backgroundColor': colors['background']}
    )
])

@app.callback(Output('my_graph','figure'),
              [Input('submit-button', 'n_clicks')],
              [State('Country', 'value'),
               State('my_date_picker', 'start_date'),
               State('my_date_picker', 'end_date')
              
              ])
         
def update_graph(n_clicks ,value, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for regions in value:
        df=df3.loc[df3['Country/Region'] ==regions]
        traces.append({ 'x': df.index, 'y': df['New cases'], 'name':regions})
        figure= {'data': traces,
        'layout':{'title': regions,
                 'yaxis' :{'title': 'New Cases'}
                 }
                 
   }
    return figure
                            
if __name__ == '__main__':
    app.run_server()
    