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
        If the atoms have charges of opposite signs, they will feel an attractive (negative) force, while if they have charges of the same sign, they will feel a repulsive (positive) force. This force is also inverseley proportional to the distance between them and the dielectric constant of the environment. Note how this force is only either always attractive or always repulsive; this is typically balanced by the Lennard-Jones interaction.
        '''
    ], style={'textAlign':'justify'}),

    html.P([
        '''
        The Coulomb interaction potential energy and force is shown in the graph below. Use the sliders to change the charges on each atom, as well as the distance between the atoms and the dielectric constant of the environment.
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
    coul_force = constant * q1 * q2 / ((r**2)*k)
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
    value=1,
    tooltip = { 'always_visible': False },
)

### Q2 SLIDER ###

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
    value=-1,
    tooltip = { 'always_visible': False },
)

### R SLIDER ###

min_r = 2  # units Angstroms
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
    value=1,
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

    fig.add_trace(
        go.Scatter(
            x=[r_value],
            y = force(q1_value, q2_value, r_value, k_value),
            mode='markers',
            marker={'color':'#E6526A', 'size':12},
        ), secondary_y=True,
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


    if min_r <= 0:
        max_pot = np.abs(potential(min_q, max_q, min_r+0.001, min_k))
    else:
        max_pot = np.abs(potential(min_q, max_q, min_r, min_k))

    nticks = 5
    dtick = [float(x) for x in
        np.format_float_scientific(max_pot).split('e')]
    dtick = math.ceil(dtick[0]*10) * 10**(int(dtick[1]-1))
    dtick = dtick/2

    fig.update_yaxes(
        secondary_y=False,
        range=[-2*dtick, 2*dtick],
        showline=True,
        mirror=True,
        ticks="outside",
        tickwidth=1,
        ticklen=10,
        linewidth=1,
        gridwidth=1,
        tickcolor='#c3c3c3',
        linecolor='#c3c3c3',
        gridcolor='#c3c3c3',
        dtick=dtick,
        title=dict(
            text='Potential Energy (kJ)',
            font=dict(
                color='#B09ADB',
            ),
        ),
        tickfont=dict(
            color='#B09ADB'
        ),
    )

    max_force = np.abs(force(min_q, max_q, min_r, min_k))
    dtick2 = [float(x) for x in
        np.format_float_scientific(max_force).split('e')]
    dtick2 = math.ceil(dtick2[0]*10) * 10**(int(dtick2[1]-1))
    dtick2 = dtick2/2

    fig.update_yaxes(
        range=[-2*dtick2, 2*dtick2],
        secondary_y=True,
        ticks="outside",
        tickwidth=1,
        ticklen=10,
        linewidth=1,
        gridwidth=1,
        tickcolor='#c3c3c3',
        linecolor='#c3c3c3',
        gridcolor='#c3c3c3',
        dtick=dtick2,
        exponentformat='e',
        title=dict(
            text='Force (N)',
            font=dict(
                color='#E2C458'
            ),
        ),
        tickfont=dict(
            color='#E2C458'
        )
    )

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

### COULOMB ATOM-FORCE PLOT ###

def update_coul_force_plot(q1_value, q2_value, r_value, k_value):

    fig = go.Figure()

    ### setting length of force vector relative to plot area and sigma

    max_force = np.abs(force(min_q, max_q, min_r, k_value))

    conversion = max_r/max_force
    mid_pt = 1 + 1 + max_r
    force_length = -conversion*force(q1_value, q2_value, r_value, k_value)
    if force(q1_value, q2_value, r_value, k_value) < 0:
        if force_length*2 > r_value:
            force_length = r_value/2

    ### atomic markers ###
    fig.add_trace(
        go.Scatter(
            x=[mid_pt - r_value/2, mid_pt + r_value/2],
            y = [1.5,1.5],
            mode='markers',
            hoverinfo='none',
            marker={'color':'#E6526A', 'size':20}
        )
    )

    ### graph layout ###
    fig.update_xaxes(
        range=[1,2+1+2*max_r],
        showline=False,
        mirror=False,
        nticks=0,
        showgrid=False,
        showticklabels=False,
    )

    fig.update_yaxes(
        range=[1.3,1.8],
        showline=False,
        mirror=False,
        nticks=0,
        showgrid=False,
        showticklabels=False,
    )

    if q1_value < 0:
        q1_sign = '-'
    elif q1_value > 0:
        q1_sign = '+'
    else:
        q1_sign = ''

    if q2_value < 0:
        q2_sign = '-'
    elif q2_value > 0:
        q2_sign = '+'
    else:
        q2_sign = ''

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        font=dict(
            color="#c3c3c3",
        ),
        title='Coulomb Interaction',
        annotations=[

            ### left force vector ###
            dict(
                x=mid_pt-r_value/2+force_length,
                y=1.5,
                xref="x",
                yref="y",
                showarrow=True,
                arrowhead=1,
                axref="x",
                ayref="y",
                ax=mid_pt-r_value/2,
                ay=1.5,
                arrowwidth=3,
                arrowcolor='#E2C458',
                arrowsize=1.2,
            ),

            ### right force vector ###
            dict(
                x=mid_pt+r_value/2-force_length,
                #x=mid_pt-r_value/2-max_force*conversion,
                y=1.5,
                xref="x",
                yref="y",
                showarrow=True,
                arrowhead=1,
                axref="x",
                ayref="y",
                ax=mid_pt+r_value/2,
                ay=1.5,
                arrowwidth=3,
                arrowcolor='#E2C458',
                arrowsize=1.2,
            ),

            ### force annotation ###
            dict(
                x=mid_pt,
                #x=mid_pt-r_value/2-max_force*conversion,
                y=1.8,
                text='Force = ' + str(
                    np.format_float_scientific(
                        force(q1_value, q2_value, r_value, k_value),
                        precision=2
                    )
                ) + ' N',
                xref="x",
                yref="y",
                showarrow=False,
                arrowhead=1,
                ax=0,
                ay=0,
                arrowwidth=3,
                arrowcolor='#E2C458',
                arrowsize=1.2,
                font=dict(
                    color='#E2C458',
                    size=16,
                ),
            ),

            # charge annotation #

            dict(
                x=mid_pt - r_value/2,
                y=1.4,
                text=q1_sign,
                xref="x",
                yref="y",
                showarrow=False,
                arrowhead=1,
                ax=0,
                ay=0,
                arrowwidth=3,
                arrowcolor='#E2C458',
                arrowsize=1.2,
                font=dict(
                    color='#c3c3c3',
                    size=16,
                ),
            ),

            dict(
                x=mid_pt + r_value/2,
                y=1.4,
                text=q2_sign,
                xref="x",
                yref="y",
                showarrow=False,
                arrowhead=1,
                ax=0,
                ay=0,
                arrowwidth=3,
                arrowcolor='#E2C458',
                arrowsize=1.2,
                font=dict(
                    color='#c3c3c3',
                    size=16,
                ),
            ),
        ],
    )

    return fig

fig  = update_coul_force_plot(coul_q1_slider.value, coul_q2_slider.value, coul_r_slider.value, coul_k_slider.value)
coul_force_plot = dcc.Graph(id='coul_force_plot',figure=fig)
