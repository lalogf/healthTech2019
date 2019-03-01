import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.tools as tls

import flask
import pandas as pd
import time
import os

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

df = pd.read_csv('https://raw.githubusercontent.com/ishanvirk/healthTech2019/master/healthData.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash('app', server=server, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Patient Metrics and Vitals'),
    html.H3('Ms. Lourie Hessel'),
    html.Div(children='''
        Age: 72
    '''),
     html.Div(children='''
        Gender: Female 
    '''),
     html.Div(children='''
        Phone: (356) 414-0145 x26339 
    '''),
     html.Div([
        html.P('ID: 862ad751-1d67-4f5a-b5ef-dd7f42165b9b'),
    ], style={'marginBottom': 50}),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Blood Pressure', 'value': 'BP'},
            {'label': 'Body Mass Index', 'value': 'BMI'},
            {'label': 'Estimated Glomerular Filteration Rate', 'value': 'GFR'},
            {'label': 'Creatinine', 'value': 'Cre'},
            {'label': 'Urea Nitrogen', 'value': 'UN'}
        ],
        value='BP'
    ),
    dcc.Graph(id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])

def update_graph(selected_dropdown_value):
    dff = df[df['Metric'] == selected_dropdown_value]
    fig = tls.make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
    fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 50, 't': 25}
    fig['layout']['showlegend'] = True

    if str(selected_dropdown_value) == 'BP':
        fig.append_trace({'x':dff.Date,'y':dff.Value1,'type':'scatter','name':'SBP mmHg'},1,1)
        fig.append_trace({'x':dff.Date,'y':dff.Value2,'type':'scatter','name':'DBP mmHg'},2,1)
    if str(selected_dropdown_value) == 'BMI':
        fig.append_trace({'x':dff.Date,'y':dff.Value1,'type':'scatter','name':'BMI kg/m2'},1,1)
    if str(selected_dropdown_value) == 'GFR':
        fig.append_trace({'x':dff.Date,'y':dff.Value1,'type':'scatter','name':'eGFR mL/min/1.73_m^2'},1,1)
    if str(selected_dropdown_value) == 'Cre':
        fig.append_trace({'x':dff.Date,'y':dff.Value1,'type':'scatter','name':'Creatinine mg/dL'},1,1)
    if str(selected_dropdown_value) == 'UN':
        fig.append_trace({'x':dff.Date,'y':dff.Value1,'type':'scatter','name':'Urea Nitrogen mg/dL'},1,1)

    
    return fig
    # dff = df[df['Metric'] == selected_dropdown_value]
    # return {
    #     'data': [{
    #         'x': dff.Date,
    #         'y': dff.Value,
    #         'x': dff.Date,
    #         'y': dff.Value2,
    #         'line': {
    #             'width': 3,
    #             'shape': 'spline'
    #         }
    #     }],
    #     'layout': {
    #         'margin': {
    #             'l': 30,
    #             'r': 20,
    #             'b': 30,
    #             't': 20
    #         }
    #     }
    # }

if __name__ == '__main__':
    app.run_server(debug=True)