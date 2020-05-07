import dash_core_components as dcc
import dash_html_components as html
import math
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as psub

### COLORS ###

#E2C458 yellow
#B09ADB purple
#E6526A pink
#c3c3c3 text

### DESCRIPTION ###

coulomb_text = html.Div([

    ### header ###
    html.H2(['Coulomb Potential']),
    html.Hr(),

    html.P([
        '''
        The Coulomb potential is used to describe non-bonded, electrostatic interactions between atoms that arise from atomic charges. The Coulomb potential is defined as:
        '''
    ], style={'textAlign':'justify'}),

    ### equation ###
    html.Div([

        html.Img(
            src='./assets/images/coulomb_equation.png',
            style={
                'height':'50px',
                'filter':'grayscale',
            },
        ),

        html.P([

            html.I('where:'),

            ### r ###
            html.P([

                html.Font('r', style={'fontFamily':'serif'}),
                ' = distance between atoms, distance units',

            ], style={'textIndent':'50px'}),

            ### q ###
            html.P([

                html.Font(['q',html.Sub('i')], style={'fontFamily':'serif'}),
                ' = partial charge of atom i, elementary charge units',

            ], style={'textIndent':'50px'}),

            ### kappa ###
            html.P([

                html.Font(['\u03BA', ], style={'fontFamily':'sans-serif'}),
                ' = dielectric constant',

            ], style={'textIndent':'50px'}),

            ### Kcoulomb ###
            html.P([

                html.Font(['K', html.Sub('Coulomb')], style={'fontFamily':'serif'}),
                ' = Coulomb constant, 8.988x10',
                html.Sup(9),
                ' N*m',
                html.Sup(2),
                '/C',
                html.Sup(2),

            ], style={'textIndent':'50px'}),

        ], style={'textAlign':'left', 'lineHeight':0.5}),

    ], style={'textAlign':'center'}),

    html.Br(),

    html.P([
        '''
        Description
        '''
    ], style={'textAlign':'justify'}),

])

### COULOMB FUNCTIONS ###

def potential(q1, q2, r, k):

    """
    returns the Coulomb potential
    """
    constant = 8.988*(10**9)
    q1 = np.copy(q1) * 1.60218e-19  # unit conversion to Coulombs
    q2 = np.copy(q2) * 1.60218e-19  # unit conversion to Coulombs
    r = np.copy(r) * 1e-10  # unit conversion to meters
    coul_pot = constant * q1 * q2 / (r*k)
    coul_pot *= 0.001  # unit conversion to kJ
    return np.array(coul_pot)

def force(q1, q2, r, k):

    "returns the force derived from the Coulomb potential (units N)"

    constant = 8.988*(10**9)
    q1 = np.copy(q1) * 1.60218e-19  # unit conversion to Coulombs
    q2 = np.copy(q2) * 1.60218e-19  # unit conversion to Coulombs
    r = np.copy(r) * 1e-10  # unit conversion to meters
    coul_force = -1 * constant * q1 * q2 / ((r**2)*k)
    return np.array(coul_force)

### Q1 SLIDER ###

min_q = -1  # units elementary charge
max_q = 1 # units elementary charge
coul_q1_slider = dcc.Slider(
    min=min_q,
    max=max_q,
    step=0.1,
    id='coul_q1_slider',
    marks={
        min_q: str(min_q),
        max_q: str(max_q),
        0: '0',
    },
    value=0.5,
    tooltip = { 'always_visible': False },
)

min_q = -1  # units elementary charge
max_q = 1 # units elementary charge
coul_q2_slider = dcc.Slider(
    min=min_q,
    max=max_q,
    step=0.1,
    id='coul_q2_slider',
    marks={
        min_q: str(min_q),
        max_q: str(max_q),
        0: '0',
    },
    value=-0.5,
    tooltip = { 'always_visible': False },
)

### R SLIDER ###

min_r = 1  # units Angstroms
max_r = 15 # units Angstroms
coul_r_slider = dcc.Slider(
    min=min_r,
    max=max_r,
    step=0.1,
    id='coul_r_slider',
    marks={
        min_r: str(min_r),
        max_r: str(max_r),
    },
    value=np.round((max_r-min_r)/2,1), # starts at optimal distance
    tooltip = { 'always_visible': False },
)

### KAPPA SLIDER ###

min_k = 1  # unitless
max_k = 100  # unitless
coul_k_slider = dcc.Slider(
    min=min_k,
    max=max_k,
    step=1,
    id='coul_k_slider',
    marks={
        min_k: str(min_k),
        max_k: str(max_k),
    },
    value=(max_k - min_k)/2,
    tooltip = { 'always_visible': False },
)

### LENNARD-JONES POTENTIAL PLOT ###

def update_coul_plot(q1_value, q2_value, r_value, k_value):

    r = np.arange(min_r,max_r,0.001)

    if r[0] == 0:
        r = r[1:]

    coul_pot = potential(q1_value, q2_value, r, k_value) # kJ
    coul_force = force(q1_value, q2_value, r, k_value) # N

    #fig = go.Figure()
    fig = psub.make_subplots(specs=[[{"secondary_y": True}]])

    ### force line ###
    fig.add_trace(
        go.Scatter(
            x=r,
            y=coul_force,
            mode='lines',
            line={'color':'#E2C458','width':5},
        ), secondary_y=True,
    )

    ### potential line ###
    fig.add_trace(
        go.Scatter(
            x=r,
            y=coul_pot,
            mode='lines',
            line={'color':'#B09ADB','width':5},
        )
    )

    ### distance marker ###
    fig.add_trace(
        go.Scatter(
            x=[r_value],
            y = potential(q1_value, q2_value, r_value, k_value),
            mode='markers',
            marker={'color':'#E6526A', 'size':12},
        )
    )

    ### graph layout ###
    fig.update_xaxes(
        range=[0, max(r)],
        showline=True,
        mirror=True,
        nticks=5,
        ticks="outside",
        tickwidth=1,
        ticklen=10,
        linewidth=1,
        gridwidth=1,
        tickcolor='#c3c3c3',
        linecolor='#c3c3c3',
        gridcolor='#c3c3c3',
    )


    # y1min = (-max_e)*2
    # y1max = max_e*3
    # nticks = 6
    # dtick = [float(x) for x in
    #     np.format_float_scientific((y1max-y1min)/nticks).split('e')]
    # dtick = math.ceil(dtick[0]) * 10**(int(dtick[1]))
    #
    # fig.update_yaxes(
    #     secondary_y=False,
    #     range=[-2*dtick, 3*dtick],
    #     showline=True,
    #     mirror=True,
    #     ticks="outside",
    #     tickwidth=1,
    #     ticklen=10,
    #     linewidth=1,
    #     gridwidth=1,
    #     tickcolor='#c3c3c3',
    #     linecolor='#c3c3c3',
    #     gridcolor='#c3c3c3',
    #     dtick=dtick,
    #     title=dict(
    #         text='Potential Energy (kJ)',
    #         font=dict(
    #             color='#B09ADB',
    #         ),
    #     ),
    #     tickfont=dict(
    #         color='#B09ADB'
    #     ),
    # )
    #
    # min_force = -1*min(force(r, min_s, max_e))
    # dtick2 = [float(x) for x in
    #     np.format_float_scientific(min_force, precision=3).split('e')]
    # dtick2 = math.ceil(dtick2[0]*10) * 10**(int(dtick2[1]-1))/2
    #
    # mask = np.where((lj_pot>= (-max_e)*1.5) & (lj_pot <= (max_e*3)))
    # min_force = min(lj_force)
    # fig.update_yaxes(
    #     range=[-2*dtick2, 3*dtick2],
    #     secondary_y=True,
    #     ticks="outside",
    #     tickwidth=1,
    #     ticklen=10,
    #     linewidth=1,
    #     gridwidth=1,
    #     tickcolor='#c3c3c3',
    #     linecolor='#c3c3c3',
    #     gridcolor='#c3c3c3',
    #     dtick=dtick2,
    #     exponentformat='e',
    #     title=dict(
    #         text='Force (N)',
    #         font=dict(
    #             color='#E2C458'
    #         ),
    #     ),
    #     tickfont=dict(
    #         color='#E2C458'
    #     )
    # )

    fig.update_layout(
        title='Coulomb Potential',
        xaxis_title="r (\u212B)",
        font=dict(
            color="#c3c3c3"
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
    )

    return fig

fig  = update_coul_plot(coul_q1_slider.value, coul_q1_slider.value, coul_r_slider.value, coul_k_slider.value)
coul_plot = dcc.Graph(id='coul_plot',figure=fig)

# ### LENNARD-JONES ATOM-FORCE PLOT ###
#
# def update_lj_force_plot(e_value, s_value, r_value):
#
#     fig = go.Figure()
#
#     ### setting length of force vector relative to plot area and sigma
#
#     opt_r = 1.122*s_value       # optimal atomic distance
#     new_r = r_value - opt_r     # relative distance compared to optimal
#     mid_pt = 2 + max_r          # mid-distance between atoms
#
#     if new_r < 0:
#         force_length = -max_r*(-new_r/(opt_r - min_r))
#     elif new_r > 0:
#         #force_length = (max_r-opt_r)*(new_r/(max_r - opt_r))/2
#         force_length = (max_r)*(new_r/(max_r - opt_r))/2
#     else:
#         force_length = 0
#
#     ### atomic markers ###
#     fig.add_trace(
#         go.Scatter(
#             x=[mid_pt - r_value/2, mid_pt + r_value/2],
#             y = [1.5,1.5],
#             mode='markers',
#             hoverinfo='none',
#             marker={'color':'#E6526A', 'size':20}
#         )
#     )
#
#     ### graph layout ###
#     fig.update_xaxes(
#         range=[1,2+1+2*max_r],
#         showline=False,
#         mirror=False,
#         nticks=0,
#         showgrid=False,
#         showticklabels=False,
#     )
#
#     fig.update_yaxes(
#         range=[1,2],
#         showline=False,
#         mirror=False,
#         nticks=0,
#         showgrid=False,
#         showticklabels=False,
#     )
#
#     fig.update_layout(
#         showlegend=False,
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         height=300,
#         font=dict(
#             color="#c3c3c3",
#         ),
#         #title='Lennard-Jones Interaction',
#         annotations=[
#
#             ### left force vector ###
#             dict(
#                 x=mid_pt-r_value/2+force_length,
#                 y=1.5,
#                 xref="x",
#                 yref="y",
#                 showarrow=True,
#                 arrowhead=1,
#                 axref="x",
#                 ayref="y",
#                 ax=mid_pt-r_value/2,
#                 ay=1.5,
#                 arrowwidth=3,
#                 arrowcolor='#E2C458',
#                 arrowsize=1.2,
#             ),
#
#             ### right force vector ###
#             dict(
#                 x=mid_pt+r_value/2-force_length,
#                 #x=mid_pt-r_value/2-max_force*conversion,
#                 y=1.5,
#                 xref="x",
#                 yref="y",
#                 showarrow=True,
#                 arrowhead=1,
#                 axref="x",
#                 ayref="y",
#                 ax=mid_pt+r_value/2,
#                 ay=1.5,
#                 arrowwidth=3,
#                 arrowcolor='#E2C458',
#                 arrowsize=1.2,
#             ),
#
#             ### force annotation ###
#             dict(
#                 x=mid_pt,
#                 #x=mid_pt-r_value/2-max_force*conversion,
#                 y=1.8,
#                 text='Force = ' + str(
#                     np.format_float_scientific(
#                         force(r_value, s_value, e_value),
#                         precision=2
#                     )
#                 ) + ' N/mol',
#                 xref="x",
#                 yref="y",
#                 showarrow=False,
#                 arrowhead=1,
#                 ax=0,
#                 ay=0,
#                 arrowwidth=3,
#                 arrowcolor='#E2C458',
#                 arrowsize=1.2,
#                 font=dict(
#                     color='#E2C458',
#                     size=16,
#                 ),
#             ),
#         ],
#     )
#
#     return fig
#
# fig  = update_lj_force_plot(lj_e_slider.value, lj_s_slider.value, lj_r_slider.value)
# lj_force_plot = dcc.Graph(id='lj_force_plot',figure=fig)
