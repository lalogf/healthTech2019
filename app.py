import os
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.tools as tls
import requests as requests
from dateutil.parser import parse
from datetime import datetime

import flask
from flask import request, render_template
import pandas as pd
import time


# server = flask.Flask('app')
# server.secret_key = os.environ.get('secret_key', 'secret')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')

r = requests.get('https://r2.smarthealthit.org/Patient/862ad751-1d67-4f5a-b5ef-dd7f42165b9b')
r2 = requests.get('https://r2.smarthealthit.org/Patient')
dropdownOptions = []


patient = r.json()
patients = r2.json().get('entry')
tableRows = []
tableRows.append(html.Tr([html.Td(patient.get('name')[0].get('given')[0]), html.Td(patient.get('name')[0].get('family')[0]) , html.Td(html.A('See patient records',href='/patient/' + patient.get('id')))]))


table_header = [
    html.Thead(html.Tr([html.Th("Name"), html.Th("Last Name"),html.Th('Detail')]))
]


for pat in patients:
    deceased = pat.get('resource').get('deceasedDateTime')
    if deceased is None :
        tableRows.append(html.Tr([html.Td(pat.get('resource').get('name')[0].get('given')[0]), html.Td(pat.get('resource').get('name')[0].get('family')[0]), html.Td(html.A('See patient records',href='/patient/' + pat.get('resource').get('id')))]))

table_body = [html.Tbody(tableRows)]

table = dbc.Table(table_header + table_body, bordered=True)


app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'



url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


patient_index = dbc.Container(
    [
    dbc.Row(
        [html.Div([
            html.H1('Patient List'),
            table
            ])
        ])])


patient_layout = dbc.Container(
    [
    dbc.Row([html.Div([
    html.H1('Patient Metrics and Vitals'),
    html.H3(patient.get('name')[0].get('prefix')[0] +  " " +patient.get('name')[0].get('given')[0] + " " + patient.get('name')[0].get('family')[0]  ),
    html.Div(children='''
        Birthday: 
    ''' + patient.get('birthDate')),
     html.Div(children='''
        Gender:  
    ''' + patient.get('gender')),
     html.Div(children='''
        Phone: 
    ''' + patient.get('telecom')[0].get('value') ),
     html.Div([
        html.P('ID: ' + patient.get('id')),
    ]),
    dcc.Dropdown(
        id='my-dropdown',
        options=dropdownOptions,
        value='Blood Pressure'
    ),
    dcc.Graph(id='my-graph')
])])])


def serve_layout():
    if flask.has_request_context():
        return url_bar_and_content_div
    return html.Div([
        url_bar_and_content_div,
        patient_index,
        patient_layout
    ])


app.layout = serve_layout

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')]) 
def display_page(pathname):
    if pathname == "/":
        return patient_index
    else:
        print(type(pathname))
        pathId = (pathname).split('/')[-1]
        print(pathId)
        patData = requests.get('https://r2.smarthealthit.org/Patient/' + pathId)
        patDataParsed = patData.json()

        if pathId == '862ad751-1d67-4f5a-b5ef-dd7f42165b9b':
          listOfCodes = ['Urea Nitrogen', 'Creatinine', 'Body Mass Index', 'Blood Pressure','Estimated Glomerular Filtration Rate']
        else:
           patientObservations = requests.get('https://r2.smarthealthit.org/Observation?subject:Patient=' + pathId+ '&_count=250')
           patientObservationsList = patientObservations.json().get('entry')
           listOfCodes = []
           for obs in patientObservationsList:
               code = obs.get('resource').get('code').get('coding')[0].get('display')
               if not code in listOfCodes:
                listOfCodes.append(code)
           
        listOfCodes.sort()
        for i in listOfCodes:
            dropdownOptions.append({'label': i, 'value': i}) 

        return dbc.Container([
                dbc.Row([html.Div([
                html.H1('Patient Metrics and Vitals'),
                html.H3('{}'.format(patDataParsed.get('name')[0].get('prefix')[0] +  " " +patDataParsed.get('name')[0].get('given')[0] + " " + patDataParsed.get('name')[0].get('family')[0])),
                html.Div(children='''
                    Birthday: 
                ''' + '{}'.format(patDataParsed.get('birthDate'))),
                 html.Div(children='''
                    Gender:  
                ''' + '{}'.format(patDataParsed.get('gender'))),
                 html.Div(children='''
                    Phone: 
                ''' + patient.get('telecom')[0].get('value') ),
                 html.Div([
                    html.P('ID: ' + '{}'.format(patDataParsed.get('id'))),
                ]),
                dcc.Dropdown(
                    id='my-dropdown',
                    options=dropdownOptions,
                    value='Blood Pressure'
                ),
                dcc.Graph(id='my-graph')])])])



@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value'), Input('url', 'pathname')])
def update_graph(selected_dropdown_value, pathname):
    pathId = (pathname).split('/')[-1]
    observationList = requests.get('https://r2.smarthealthit.org/Observation?subject:Patient='+ pathId+'&_count=250')
    observations = observationList.json().get('entry')
    labList = {
    'Unit': '',
    'Value1': [],
    'Value2': [], 
    'Date': []
    }
    fig = tls.make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
    fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 50, 't': 25}
    fig['layout']['showlegend'] = True
    if selected_dropdown_value == 'Blood Pressure':
        for ob in observations:
            if ob.get('resource').get('code').get('coding')[0].get('display') == selected_dropdown_value:
                s = str((parse(ob.get('resource').get('effectiveDateTime'))))
                labList.get('Date').append(s.split(' ')[0])
                labList.get('Value1').append(ob.get('resource').get('component')[0].get('valueQuantity').get('value'))
                labList.get('Value2').append(ob.get('resource').get('component')[1].get('valueQuantity').get('value'))
                unitItem = ob.get('resource').get('component')[0].get('valueQuantity').get('unit')
                labList.update({'Unit': unitItem})
        v = labList.get('Value1')
        v2 = labList.get('Value2')
        d = labList.get('Date')        
        keydict = dict(zip(v,d))
        keydict2 = dict(zip(v2,d))
        v.sort(key=keydict.get)
        v2.sort(key=keydict2.get)
        d.sort()
        fig.append_trace({'x':labList['Date'],'y':labList['Value1'],'type':'scatter','name': 'SBP ' + labList['Unit'] },1,1)
        fig.append_trace({'x':labList['Date'],'y':labList['Value2'],'type':'scatter','name':'DBP ' + labList['Unit']},1,1)
    else:
        for ob in observations:
            if ob.get('resource').get('code').get('coding')[0].get('display') == selected_dropdown_value:
                labList.get('Value1').append(ob.get('resource').get('valueQuantity').get('value'))
                labList.get('Date').append(parse(ob.get('resource').get('effectiveDateTime')))
                unitItem = ob.get('resource').get('valueQuantity').get('unit')
                labList.update({'Unit': unitItem})
        v = labList.get('Value1')
        d = labList.get('Date')        
        keydict = dict(zip(v,d))
        v.sort(key=keydict.get)
        d.sort()      
        fig.append_trace({'x':labList['Date'],'y':labList['Value1'],'type':'scatter','name':labList['Unit']},1,1)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)