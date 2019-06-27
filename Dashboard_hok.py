#!/usr/bin/env python
# coding: utf-8
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from flask import Flask
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


df = pd.read_csv("/mnt/c/Users/HCD/insight_DS/dashboard/h_dashboard/cust_type_clay.csv")
df2=pd.read_csv("/mnt/c/Users/HCD/insight_DS/dashboard/h_dashboard/cust_type_nb.csv")
df3=pd.read_csv("/mnt/c/Users/HCD/insight_DS/dashboard/h_dashboard/cust_type_sgv.csv")
df4=pd.read_csv("/mnt/c/Users/HCD/insight_DS/dashboard/h_dashboard/number_cust_nyc_fok.csv")


app = dash.Dash()

all_options = {
    'West side': ['CityA', 'CityB'],
    'East side': ['CityC'],
    'All': ['CityC', 'CityA', 'CityB']
}


city_data = {
    'CityA': {'x': df3["cust_type"].tolist(), 'y': df3['number_meter'].tolist()},
    'CityB': {'x': df2["cust_type"].tolist(), 'y':df2['Number_of_meter'].tolist()},
    #'New York City': {'x': df4["cust_type"].tolist(), 'y': df4['number_meter'].tolist()},
    'CityC': {'x':df["cust_type"].tolist(), 'y': df['Number_of_meter'].tolist()}
    
}



#trace1 = go.Bar(x=df["cust_type"], y=df['Number_of_meter'],name='Meter quantity by cust_type in Clayton county')
#trace2 = go.Scatter(x=df2["cust_type"], y=df2['Number_of_meter'],name='Meter quantity by cust_type in newport beach')
#trace3 = go.Bar(x=df3["cust_type"], y=df3['number_meter'],name='Meter quantity by cust_type in sgv')
#trace4 = go.Bar(x=df4["cust_type"], y=df4['number_meter'],name='Meter quantity by cust_type in New york city')

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'}) 


app.layout = html.Div(
     html.Div([
        html.Div(
            [
                html.H1(children='Missing Water',
                        className='nine columns'),
                html.Img(
                    src="https://files.startupranking.com/startup/thumb/52244_72510a0ea0ae0f4196b76e942a975baf592967ef_insight-data-science_m.png",
                    className='three columns',
                    style={
                        'height': '9%',
                        'width': '9%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 0,
                        'padding-right': 0
                    },
                ),
				
				 
                html.Div(children='''
                         A dashboard to present the water usage conditions from water meter in the big island.
                        ''',
                        className='nine columns'
                )
            ], className="row"
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose City:'),
                        dcc.Checklist(
                                id = 'Cities',
                                options=[
                                    {'label': 'CityB', 'value': 'CityB'},
									{'label': 'CityA', 'value': 'CityA'},
                                    {'label': 'CityC', 'value': 'CityC'}
                                ],
                                values=['CityB','CityA','CityC'],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Choose Region:'),
                        dcc.RadioItems(
                                id = 'Country',
                                options=[{'label': k, 'value': k} for k in all_options.keys()],
                                value='All',
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )
            ], className="row"
        ),
	
    html.Div([
		html.Div([
			dcc.Graph(
        id='example-graph',
        )
	],className= 'six columns'
	),
		html.Div([
            dcc.Graph(
        id='example-graph-2'
        )
    ], className= 'six columns'
    )
	],className="row"
	)
   ], className='ten columns offset-by-one')
) 
 

@app.callback(
    dash.dependencies.Output('Cities', 'options'),
    [dash.dependencies.Input('Country', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('Cities', 'values')])
def update_image_src(selector):
    data = []
    for city in selector:
        data.append({'x': city_data[city]['x'], 'y': city_data[city]['y'],
                    'type': 'bar', 'name': city})
    figure = {
        'data': data,
        'layout': {
            'title': 'Bar graph',
            'xaxis' : dict(
                title='customer type',
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                title='number of water meter',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'
            ))
        }
    }
    return figure

@app.callback(
    dash.dependencies.Output('example-graph-2', 'figure'),
    [dash.dependencies.Input('Cities', 'values')])
def update_image_src(selector):
    data = []
    for city in selector:
        data.append({'x': city_data[city]['x'], 'y': city_data[city]['y'],
                    'type': 'line', 'name': city})
    figure = {
        'data': data,
        'layout': {
            'title': 'Line plot',
            'xaxis' : dict(
                title='customer type',
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                title='number of water meter',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'
            ))
        }
    }
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)







