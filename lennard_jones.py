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

lj_text = html.Div([

    ### header ###
    html.H2(['Lennard-Jones Potential']),
    html.Hr(),

    html.P([
        '''
        The Lennard-Jones potential is used to describe non-bonded interactions between atoms that arise from van der Waals forces and steric repulsion. The Lennard-Jones potential is defined as:
        '''
    ], style={'textAlign':'justify'}),

    ### equation ###
    html.Div([

        html.Img(
            src='./assets/images/lj_equation.png',
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

            ### sigma ###
            html.P([

                html.Font('\u03C3', style={'fontFamily':'serif'}),
                ' = distance constant, distance units',

            ], style={'textIndent':'50px'}),

            ### epsilon ###
            html.P([

                html.Font(['\u025B'], style={'fontFamily':'serif'}),
                ' = energy constant related to strength of the interaction, energy units',

            ], style={'textIndent':'50px'}),

        ], style={'textAlign':'left', 'lineHeight':0.5}),

    ], style={'textAlign':'center'}),

    html.Br(),

    html.P([
        '''
        The first term (power of 12) is the repulsive part of the interaction due to steric forces. This occurs when the electron clouds of two approaching atoms get too close. There is a steep increase in potential energy and the atoms feel a strong repulsive force pushing them away from each other. The second term (power of 6) is the attractive part of the interaction due to van der Waals forces. These arise from dipole-dipole interactions, dipole-induced dipole interactions, and London/dispersion forces, which have electrostatic and quantum mechanical origins. When the atoms are reasonably far from each other, they feel a small attractive force pulling them closer to each other towards their optimal distance.
        '''
    ], style={'textAlign':'justify'}),

    html.P([
        '''
        The Lennard-Jones potential energy and force is shown in the graph below. Use the sliders to change the distance between the atoms, as well as the \u03C3 (distance) and \u025B (energy) parameters. You can also observe two atoms and the force that each of them 'feels' as they move closer or farther apart. The optimal distance for the two atoms is found at the bottom of the 'well' in the Lennard-Jones potential, and therefore, the force vector is equal to zero at that location. At positions closer than this distance, the force vector is positive (repulsive) and at positions farther than this distance, the force vector is negative (attractive). Note how the force on the atoms reduces quickly the farther away the atoms get from each other (limited range of the interaction). Also note how strong the repulsive force quickly becomes as the atoms move close together as a result of the strong, steric repulsion of the atoms.
        '''
    ], style={'textAlign':'justify'}),

])

### LENNARD-JONES FUNCTIONS ###

def potential(r, sigma, epsilon):

    """
    returns the Lennard-Jones potential
    """

    lj_pot = 4 * epsilon * ((sigma/r)**12 - (sigma/r)**6)
    return np.array(lj_pot)

def force(r, sigma, epsilon):

    "returns the force derived from the Lennard-Jones potential (units N)"

    lj_force = -4 * epsilon * (sigma**12*(-12)*r**(-13) - sigma**6*(-6)*r**(-7))
    lj_force *= 1e13 # change kj/mol-Ang to N/mol
    return np.array(lj_force)

### SIGMA SLIDER ###

min_s = 1  # units Angstroms
max_s = 15 # units Angstroms
lj_s_slider = dcc.Slider(
    min=min_s,
    max=max_s,
    step=0.1,
    id='lj_s_slider',
    marks={
        min_s: str(min_s),
        max_s: str(max_s),
    },
    value=(max_s - min_s)/2,
    tooltip = { 'always_visible': False },
)

### R SLIDER ###

min_r = 1  # units Angstroms
max_r = 15 # units Angstroms
lj_r_slider = dcc.Slider(
    min=min_r,
    max=max_r,
    step=0.1,
    id='lj_r_slider',
    marks={
        min_r: str(min_r),
        max_r: str(max_r),
    },
    value=np.round(1.122*lj_s_slider.value,1), # starts at optimal distance
    tooltip = { 'always_visible': False },
)

### EPSILON SLIDER ###

min_e = 0  # units kJ
max_e = 5  # units kJ
lj_e_slider = dcc.Slider(
    min=min_e,
    max=max_e,
    step=0.0001,
    id='lj_e_slider',
    marks={
        min_e: str(min_e),
        max_e: str(max_e),
    },
    value=(max_e - min_e)/2,
    tooltip = { 'always_visible': False },
)

### LENNARD-JONES POTENTIAL PLOT ###

def update_lj_plot(e_value, s_value, r_value):

    r = np.arange(min_r,max_r,0.001)
    if r[0] == 0:
        r = r[1:]

    lj_pot = potential(r, s_value, e_value) # kJ/mol
    lj_force = force(r, s_value, e_value) # N/mol

    #fig = go.Figure()
    fig = psub.make_subplots(specs=[[{"secondary_y": True}]])

    ### force line ###
    fig.add_trace(
        go.Scatter(
            x=r,
            y=lj_force,
            mode='lines',
            line={'color':'#E2C458','width':5},
        ), secondary_y=True,
    )

    ### potential line ###
    fig.add_trace(
        go.Scatter(
            x=r,
            y=lj_pot,
            mode='lines',
            line={'color':'#B09ADB','width':5},
        )
    )

    ### distance marker ###
    fig.add_trace(
        go.Scatter(
            x=[r_value],
            y = potential(r_value, s_value, e_value),
            mode='markers',
            marker={'color':'#E6526A', 'size':12},
        )
    )

    ### graph layout ###
    fig.update_xaxes(
        range=[0,max(r)],
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


    y1min = (-max_e)*2
    y1max = max_e*3
    nticks = 6
    dtick = [float(x) for x in
        np.format_float_scientific((y1max-y1min)/nticks).split('e')]
    dtick = math.ceil(dtick[0]) * 10**(int(dtick[1]))

    fig.update_yaxes(
        secondary_y=False,
        range=[-2*dtick, 3*dtick],
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
            text='Potential Energy (kJ/mol)',
            font=dict(
                color='#B09ADB',
            ),
        ),
        tickfont=dict(
            color='#B09ADB'
        ),
    )

    min_force = -1*min(force(r, min_s, max_e))
    dtick2 = [float(x) for x in
        np.format_float_scientific(min_force, precision=3).split('e')]
    dtick2 = math.ceil(dtick2[0]*10) * 10**(int(dtick2[1]-1))/2

    mask = np.where((lj_pot>= (-max_e)*1.5) & (lj_pot <= (max_e*3)))
    min_force = min(lj_force)
    fig.update_yaxes(
        range=[-2*dtick2, 3*dtick2],
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
            text='Force (N/mol)',
            font=dict(
                color='#E2C458'
            ),
        ),
        tickfont=dict(
            color='#E2C458'
        )
    )

    fig.update_layout(
        title='Lennard-Jones Potential',
        xaxis_title="r (\u212B)",
        font=dict(
            color="#c3c3c3"
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
    )

    return fig

fig  = update_lj_plot(lj_e_slider.value, lj_s_slider.value, lj_r_slider.value)
lj_plot = dcc.Graph(id='lj_plot',figure=fig)

### LENNARD-JONES ATOM-FORCE PLOT ###

def update_lj_force_plot(e_value, s_value, r_value):

    fig = go.Figure()

    ### setting length of force vector relative to plot area and sigma

    opt_r = 1.122*s_value       # optimal atomic distance
    new_r = r_value - opt_r     # relative distance compared to optimal
    mid_pt = 2 + max_r          # mid-distance between atoms

    if new_r < 0:
        force_length = -max_r*(-new_r/(opt_r - min_r))
    elif new_r > 0:
        #force_length = (max_r-opt_r)*(new_r/(max_r - opt_r))/2
        force_length = (max_r)*(new_r/(max_r - opt_r))/2
    else:
        force_length = 0

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
        range=[1,2],
        showline=False,
        mirror=False,
        nticks=0,
        showgrid=False,
        showticklabels=False,
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        font=dict(
            color="#c3c3c3",
        ),
        #title='Lennard-Jones Interaction',
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
                        force(r_value, s_value, e_value),
                        precision=2
                    )
                ) + ' N/mol',
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
        ],
    )

    return fig

fig  = update_lj_force_plot(lj_e_slider.value, lj_s_slider.value, lj_r_slider.value)
lj_force_plot = dcc.Graph(id='lj_force_plot',figure=fig)
