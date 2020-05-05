import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

import lennard_jones as lj
import header
import introduction as intro
import force_fields as ff

import plotly.express as px



app = dash.Dash(__name__,external_stylesheets=[dbc.themes.GRID])

app.layout = html.Div([

    ### HEADER ###
    html.Div([
        html.Img(src='assets/images/cei-logo.png', style={'height':'100px'})
    ], style={'textAlign':'center'}),
    header.header_text,

    ### INTRODUCTION ###
    html.Div([intro.intro_text], className='float'),

    ### FORCE FIELDS ###
    html.Div([ff.ff_text], className='float'),

    ### LENNARD-JONES POTENTIAL ###
    html.Div([

        lj.lj_text,

        html.Br(),

    ], className='float'),

    html.Div([

        html.Div([

            html.Div([

                html.Div([
                    html.Div(['r (\u212B)'], className = 'col-sm-3', style={'textAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        lj.lj_r_slider,
                    ], className = 'col-sm-9', style={'verticalAlign':'center'}),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

                html.Div([
                    html.Label(['\u03C3 (\u212B)'], className = 'col-sm-3', style={'textAlign':'center', 'verticalAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        lj.lj_s_slider,
                    ], className = 'col-sm-9'),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

                html.Div([
                    html.Label(['\u025B (kcal/mol)'], className = 'col-sm-3', style={'textAlign':'center', 'verticalAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        lj.lj_e_slider,
                    ], className = 'col-sm-9'),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

            ], className = 'float', style={'verticalAlign':'center'}),

            html.Div([

                lj.lj_force_plot,

            ], className = 'float', style={'height':'290px'}),

        ], className='col-sm-6'),

        html.Div([

            html.Div([

                lj.lj_plot,

            ], className = 'float', style={}),

        ], className='col-sm-6'),
    ], className='row'),
])

### UPDATE LENNARD-JONES POTENTIAL PLOT ###

@app.callback(Output('lj_plot', 'figure'),
             [Input('lj_e', 'value'),
             Input('lj_s', 'value'),
             Input('lj_r', 'value')])
def update_lj_plot(e_value, s_value, r_value):
    return lj.update_lj_plot(e_value, s_value, r_value)

@app.callback(Output('lj_force_plot', 'figure'),
             [Input('lj_e', 'value'),
             Input('lj_s', 'value'),
             Input('lj_r', 'value')])
def update_lj_force_plot(e_value, s_value, r_value):
    return lj.update_lj_force_plot(e_value, s_value, r_value)

# set debug=False when not in development
if __name__ == '__main__':
    app.run_server(debug=True)
