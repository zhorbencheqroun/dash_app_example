
# coding: utf-8

# In[ ]:

import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df=pd.read_csv('nama_10_gdp_1_Data.csv')

available_indicators = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df1 = df[df['UNIT'] == 'Current prices, million euro']

app.layout = html.Div([
     html.Div(
         [html.Div([
            dcc.Dropdown( id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
         style={'width': '30%', 'display': 'inline-block'}),
             
            html.Div([
            dcc.Dropdown( 
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries'
            )
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
    ]),
      dcc.Graph(id='grph1'),
    
    html.Div(dcc.Slider( 
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in df['TIME'].unique()},
    
    ), style={'marginRight': 50, 'marginLeft': 110},),

    html.Div([
        html.Div([
            dcc.Dropdown( id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),
        
         html.Div([
            dcc.Dropdown( 
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= "Spain"
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
       dcc.Graph(id='grph2'),
    
])
    
@app.callback(
    dash.dependencies.Output('grph1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    df_yearly = df[df['TIME'] == year_value]
    return {
        'data': [go.Scatter(
            x=df_yearly[df_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            y=df_yearly[df_yearly['NA_ITEM'] == yaxis_column_name]['Value'],
            text=df_yearly[df_yearly['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }
    
@app.callback(
    dash.dependencies.Output('grph2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name):
    df_yearly = df1[df1['GEO'] == yaxis_column_name] 
    return {
        'data': [go.Scatter(
            x=df_yearly['TIME'].unique(),
            y=df_yearly[df_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }
   
if __name__ == '__main__':
    app.run_server()
    

