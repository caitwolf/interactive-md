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
import bonds as bond
import angles as angle
import coulomb as coul
import references as ref

import plotly.express as px



app = dash.Dash(__name__,external_stylesheets=[dbc.themes.GRID])

# server = app.server
#
# app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

app.layout = html.Div([

    ### HEADER ###
    header.header_text,

    # ### INTRODUCTION ###
    # html.Div([intro.intro_text], className='float'),

    ### FORCE FIELDS ###
    html.Div([ff.ff_text], className='float'),

    ### BOND POTENTIAL ###
    html.Div([

        bond.bond_text,

        html.Br(),

    ], className='float'),

    html.Div([

        html.Div([

            html.Div([

                html.Div([
                    html.Div(['b (\u212B)'], className = 'col-sm-3', style={'textAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        bond.bond_b_slider,
                    ], className = 'col-sm-9', style={'verticalAlign':'center'}),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

                html.Div([
                    html.Label(['b', html.Sub('o'), ' (\u212B)'], className = 'col-sm-3', style={'textAlign':'center', 'verticalAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        bond.bond_bo_slider,
                    ], className = 'col-sm-9'),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

                html.Div([
                    html.Label(['K', html.Sub('b'),' (kJ/(mol*\u212B',html.Sup('2'),'))'], className = 'col-sm-3', style={'textAlign':'center', 'verticalAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        bond.bond_kb_slider,
                    ], className = 'col-sm-9'),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

            ], className = 'float', style={'verticalAlign':'center'}),

            html.Div([

                bond.bond_force_plot,

            ], className = 'float', style={'height':'290px'}),

        ], className='col-sm-6'),

        html.Div([

            html.Div([

                bond.bond_plot,

            ], className = 'float', style={}),

        ], className='col-sm-6'),

    ], className='row'),

    ### ANGLE POTENTIAL ###
    html.Div([

        angle.angle_text,

        html.Br(),

    ], className='float'),

    html.Div([

        html.Div([

            html.Div([

                html.Div([
                    html.Div(['\u03B8 (degrees)'], className = 'col-sm-4', style={'textAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        angle.angle_th_slider,
                    ], className = 'col-sm-8', style={'verticalAlign':'center'}),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

                html.Div([
                    html.Label(['\u03B8', html.Sub('o'), ' (degrees)'], className = 'col-sm-4', style={'textAlign':'center', 'verticalAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        angle.angle_tho_slider,
                    ], className = 'col-sm-8'),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

                html.Div([
                    html.Label(['K', html.Sub('\u03B8'),' (kJ/(mol*degrees',html.Sup('2'),'))'], className = 'col-sm-4', style={'textAlign':'center', 'verticalAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        angle.angle_kth_slider,
                    ], className = 'col-sm-8'),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

            ], className = 'float', style={'verticalAlign':'center'}),

            html.Div([

                angle.angle_force_plot,

            ], className = 'float', style={'height':'290px'}),

        ], className='col-sm-6'),

        html.Div([

            html.Div([

                angle.angle_plot,

            ], className = 'float', style={}),

        ], className='col-sm-6'),
    ], className='row'),

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
                    html.Label(['\u025B (kJ/mol)'], className = 'col-sm-3', style={'textAlign':'center', 'verticalAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
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

    ### COULOMB POTENTIAL ###
    html.Div([

        coul.coulomb_text,

        html.Br(),

    ], className='float'),

    html.Div([

        html.Div([

            html.Div([

                html.Div([
                    html.Div(['q', html.Sub('1'),' (e)'], className = 'col-sm-3', style={'textAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        coul.coul_q1_slider,
                    ], className = 'col-sm-9', style={'verticalAlign':'center'}),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

                html.Div([
                    html.Div(['q', html.Sub('2'),' (e)'], className = 'col-sm-3', style={'textAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        coul.coul_q2_slider,
                    ], className = 'col-sm-9', style={'verticalAlign':'center'}),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

                html.Div([
                    html.Label(['r (\u212B)'], className = 'col-sm-3', style={'textAlign':'center', 'verticalAlign':'center', 'fontFamily':'serif', 'fontSize':'16px'}),
                    html.Div([
                        coul.coul_r_slider,
                    ], className = 'col-sm-9'),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

                html.Div([
                    html.Label(['\u03BA'], className = 'col-sm-3', style={'textAlign':'center', 'verticalAlign':'center', 'fontFamily':'sans-serif', 'fontSize':'16px'}),
                    html.Div([
                        coul.coul_k_slider,
                    ], className = 'col-sm-9'),
                ], className = 'row', style={'verticalAlign':'center','height':'50px', 'padding': '15px 0'}),

            ], className = 'float', style={'verticalAlign':'center'}),

            html.Div([

                coul.coul_force_plot,

            ], className = 'float', style={'height':'240px'}),

        ], className='col-sm-6'),

        html.Div([

            html.Div([

                coul.coul_plot,

            ], className = 'float', style={}),

        ], className='col-sm-6'),
    ], className='row'),

    # ### REFERENCES ###
    html.Div([ref.refs], className='float'),

])

### UPDATE LENNARD-JONES POTENTIAL PLOT ###

@app.callback(Output('lj_plot', 'figure'),
             [Input('lj_e_slider', 'value'),
             Input('lj_s_slider', 'value'),
             Input('lj_r_slider', 'value')])
def update_lj_plot(e_value, s_value, r_value):
    return lj.update_lj_plot(e_value, s_value, r_value)

### UPDATE LENNARD-JONES ATOM-FORCE PLOT ###

@app.callback(Output('lj_force_plot', 'figure'),
             [Input('lj_e_slider', 'value'),
             Input('lj_s_slider', 'value'),
             Input('lj_r_slider', 'value')])
def update_lj_force_plot(e_value, s_value, r_value):
    return lj.update_lj_force_plot(e_value, s_value, r_value)

### UPDATE COULOMB POTENTIAL PLOT ###

@app.callback(Output('coul_plot', 'figure'),
             [Input('coul_q1_slider', 'value'),
             Input('coul_q2_slider', 'value'),
             Input('coul_r_slider', 'value'),
             Input('coul_k_slider', 'value')])
def update_coul_plot(q1_value, q2_value, r_value, k_value):
    return coul.update_coul_plot(q1_value, q2_value, r_value, k_value)

### UPDATE COULOMB ATOM-FORCE PLOT ###

@app.callback(Output('coul_force_plot', 'figure'),
             [Input('coul_q1_slider', 'value'),
             Input('coul_q2_slider', 'value'),
             Input('coul_r_slider', 'value'),
             Input('coul_k_slider', 'value')])
def update_coul_force_plot(q1_value, q2_value, r_value, k_value):
    return coul.update_coul_force_plot(q1_value, q2_value, r_value, k_value)

### UPDATE BONDED POTENTIAL PLOT ###

@app.callback(Output('bond_plot', 'figure'),
             [Input('bond_b_slider', 'value'),
             Input('bond_bo_slider', 'value'),
             Input('bond_kb_slider', 'value')])
def update_bond_plot(b_value, bo_value, kb_value):
    return bond.update_bond_plot(b_value, bo_value, kb_value)

### UPDATE BONDED ATOM-FORCE PLOT ###

@app.callback(Output('bond_force_plot', 'figure'),
             [Input('bond_b_slider', 'value'),
             Input('bond_bo_slider', 'value'),
             Input('bond_kb_slider', 'value')])
def update_bond_force_plot(b_value, bo_value, kb_value):
    return bond.update_bond_force_plot(b_value, bo_value, kb_value)

### UPDATE ANGLE POTENTIAL PLOT ###

@app.callback(Output('angle_plot', 'figure'),
             [Input('angle_th_slider', 'value'),
             Input('angle_tho_slider', 'value'),
             Input('angle_kth_slider', 'value')])
def update_angle_plot(th_value, tho_value, kth_value):
    return angle.update_angle_plot(th_value, tho_value, kth_value)

### UPDATE ANGLE ATOM-FORCE PLOT ###

@app.callback(Output('angle_force_plot', 'figure'),
             [Input('angle_th_slider', 'value'),
             Input('angle_tho_slider', 'value'),
             Input('angle_kth_slider', 'value')])
def update_angle_force_plot(th_value, tho_value, kth_value):
    return angle.update_angle_force_plot(th_value, tho_value, kth_value)


# set debug=False when not in development
if __name__ == '__main__':
    app.run_server(debug=True)
