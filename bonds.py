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

bond_text = html.Div([

    ### header ###
    html.H2(['Bonded Potential']),
    html.Hr(),

    html.P([
        '''
        The bonded potential takes the form of a harmonic, similar to that of a spring:
        '''
    ], style={'textAlign':'justify'}),

    ### equation ###
    html.Div([

        html.Img(
            src='./assets/images/bonds_equation.png',
            style={
                'height':'50px',
                'filter':'grayscale',
            },
        ),

        html.P([

            html.I('where:'),

            ### b ###
            html.P([

                html.Font('b', style={'fontFamily':'serif'}),
                ' = distance between atoms, distance units',

            ], style={'textIndent':'50px'}),

            ### bo ###
            html.P([

                html.Font(['b', html.Sub('o')], style={'fontFamily':'serif'}),
                ' = bond distance constant, distance units',

            ], style={'textIndent':'50px'}),

            ### Kb ###
            html.P([

                html.Font(['K', html.Sub('b')], style={'fontFamily':'serif'}),
                ' = bonded constant related to strength of the interaction, energy/distance', html.Sup('2'),' units',

            ], style={'textIndent':'50px'}),

        ], style={'textAlign':'left', 'lineHeight':0.5}),

    ], style={'textAlign':'center'}),

    html.Br(),

    html.P([
        '''
        The optimal bond distance is found at the bottom of the well in the harmonic bonded potential profile. At this point, the force vector is zero. However, as the atoms get closer together, they feel a repulsive (positive) force, and as the atoms get farther away, they feel a proportionally strong attractive force (negative). Note the symmetric nature of this potential. The bonded potential energy and force are shown in the graph below. Use the sliders to change the distance between the atoms, as well as the bo and Kb parameters. You can observe how modifying the Kb forth change the strength of the interaction.
        '''
    ], style={'textAlign':'justify'}),

])

### BONDED INTERACTION FUNCTIONS ###

def potential(b, bo, kb):

    """
    returns the bond potential
    """

    bond_pot = 0.5 * kb * (b-bo)**2
    return np.array(bond_pot)

def force(b, bo, kb):

    "returns the force derived from the Lennard-Jones potential (units N)"

    bond_force = -kb * (b-bo)
    bond_force *= 1e13 # change kj/mol-Ang to N/mol
    return np.array(bond_force)

### Bo SLIDER ###

min_bo = 1  # units Angstroms
max_bo = 15 # units Angstroms
bond_bo_slider = dcc.Slider(
    min=min_bo,
    max=max_bo,
    step=0.1,
    id='bond_bo_slider',
    marks={
        min_bo: str(min_bo),
        max_bo: str(max_bo),
    },
    value=np.round((max_bo-min_bo)/2,1), # starts at optimal distance
    tooltip = { 'always_visible': False },
)

### B SLIDER ###

min_b = 1  # units Angstroms
max_b = 15 # units Angstroms
bond_b_slider = dcc.Slider(
    min=min_b,
    max=max_b,
    step=0.1,
    id='bond_b_slider',
    marks={
        min_b: str(min_b),
        max_b: str(max_b),
    },
    value=np.round(bond_bo_slider.value,1), # starts at optimal distance
    tooltip = { 'always_visible': False },
)

### Kb SLIDER ###

min_kb = 100  # units kJ/mol
max_kb = 1000  # units kJ/mol
bond_kb_slider = dcc.Slider(
    min=min_kb,
    max=max_kb,
    step=0.0001,
    id='bond_kb_slider',
    marks={
        min_kb: str(min_kb),
        max_kb: str(max_kb),
    },
    value=(max_kb - min_kb)/2,
    tooltip = { 'always_visible': False },
)

### BOND POTENTIAL PLOT ###

def update_bond_plot(b_value, bo_value, kb_value):

    b = np.arange(min_b,max_b,0.001)
    if b[0] == 0:
        b = b[1:]

    bond_pot = potential(b, bo_value, kb_value) # kJ/mol
    bond_force = force(b, bo_value, kb_value) # N/mol

    #fig = go.Figure()
    fig = psub.make_subplots(specs=[[{"secondary_y": True}]])

    ### force line ###
    fig.add_trace(
        go.Scatter(
            x=b,
            y=bond_force,
            mode='lines',
            line={'color':'#E2C458','width':5},
        ), secondary_y=True,
    )

    ### potential line ###
    fig.add_trace(
        go.Scatter(
            x=b,
            y=bond_pot,
            mode='lines',
            line={'color':'#B09ADB','width':5},
        )
    )

    ### distance marker ###
    fig.add_trace(
        go.Scatter(
            x=[b_value],
            y = potential(b_value, bo_value, kb_value),
            mode='markers',
            marker={'color':'#E6526A', 'size':12},
        )
    )

    ### distance marker 2 ###
    fig.add_trace(
        go.Scatter(
            x=[b_value],
            y = force(b_value, bo_value, kb_value),
            mode='markers',
            marker={'color':'#E6526A', 'size':12},
        ), secondary_y=True,
    )

    ### graph layout ###
    fig.update_xaxes(
        range=[0,max(b)],
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


    max_pot = potential(min_b, max_bo, max_kb)
    dtick = [float(x) for x in
        np.format_float_scientific(max_pot/3).split('e')]
    dtick = math.ceil(dtick[0]) * 10**int(dtick[1])

    fig.update_yaxes(
        secondary_y=False,
        range=[-dtick, dtick*3],
        showline=True,
        mirror=True,
        ticks="outside",
        tickwidth=1,
        ticklen=10,
        linewidth=1,
        gridwidth=1,
        exponentformat='e',
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

    max_force = force(min_b, max_bo, max_kb)
    dtick2 = [float(x) for x in
        np.format_float_scientific(max_force).split('e')]
    dtick2 = math.ceil(dtick2[0]) * 10**int(dtick2[1])/2


    fig.update_yaxes(
        #range=[-2*dtick2, 3*dtick2],
        range=[-dtick2*2, dtick2*2],
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
        title='Bond Potential',
        xaxis_title="r (\u212B)",
        font=dict(
            color="#c3c3c3"
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
    )

    return fig

fig  = update_bond_plot(bond_b_slider.value, bond_bo_slider.value, bond_kb_slider.value)
bond_plot = dcc.Graph(id='bond_plot',figure=fig)

### BONDED ATOM-FORCE PLOT ###

def update_bond_force_plot(b_value, bo_value, kb_value):

    fig = go.Figure()

    mid_pt = 1 + 1 + max_b

    ### atomic markers ###
    fig.add_trace(
        go.Scatter(
            x=[mid_pt - b_value/2, mid_pt + b_value/2],
            y = [1.5,1.5],
            mode='markers',
            hoverinfo='none',
            marker={'color':'#E6526A', 'size':20}
        )
    )

    ### spring ###

    r = 0.25
    tie_len = 1

    x = np.arange(0,r*2,0.001)
    y = r+np.sqrt(r**2 - (x-r)**2)

    x2 = np.arange(r*2,0,-0.001)
    y2 = r-np.sqrt(r**2 - (x-r)**2)

    x = np.hstack((x,x2)) + np.linspace(0,r,len(x)*2)
    y = np.hstack((y,y2))

    xplot = np.array([])
    yplot = np.array([])

    xplot = np.hstack((xplot,x))
    yplot = np.hstack((yplot,y))

    for coil in range(0,2):
        x_step = xplot[-1]
        xplot = np.hstack((xplot,x+x_step))
        yplot = np.hstack((yplot,y))

    x_step = xplot[-1]
    half = int(len(x)/2)+1
    xplot = np.hstack((xplot,x[:half]+x_step))
    yplot = np.hstack((yplot,y[:half]))

    spring_len = b_value - 2*tie_len
    xplot = tie_len + xplot*spring_len/max(xplot) + mid_pt - 0.5*spring_len - tie_len
    yplot = yplot - r + 1.5

    fig.add_trace(
        go.Scatter(
            x=xplot,
            y=yplot,
            hoverinfo='none',
            mode='lines',
            line={'color':"#c3c3c3",'width':3},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[mid_pt-b_value/2,mid_pt-b_value/2+tie_len],
            y=[1.5,1.5],
            hoverinfo='none',
            mode='lines',
            line={'color':"#c3c3c3",'width':3},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[mid_pt+b_value/2-tie_len,mid_pt+b_value/2],
            y=[1.5,1.5],
            hoverinfo='none',
            mode='lines',
            line={'color':"#c3c3c3",'width':3},
        )
    )

    ### graph layout ###
    fig.update_xaxes(
        range=[1,2+1+2*max_b],
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

    max_force = force(min_b, max_bo, kb_value)
    conversion = (max_b-min_b)/(1.1*max_force)
    force_length = -1*force(b_value, bo_value, kb_value)*conversion

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        font=dict(
            color="#c3c3c3",
        ),
        title='Bond Interaction',
        annotations=[

            ### left force vector ###
            dict(
                x=mid_pt-b_value/2+force_length,
                y=1.5,
                xref="x",
                yref="y",
                showarrow=True,
                arrowhead=1,
                axref="x",
                ayref="y",
                ax=mid_pt-b_value/2,
                ay=1.5,
                arrowwidth=3,
                arrowcolor='#E2C458',
                arrowsize=1.2,
            ),

            ### right force vector ###
            dict(
                x=mid_pt+b_value/2-force_length,
                #x=mid_pt-r_value/2-max_force*conversion,
                y=1.5,
                xref="x",
                yref="y",
                showarrow=True,
                arrowhead=1,
                axref="x",
                ayref="y",
                ax=mid_pt+b_value/2,
                ay=1.5,
                arrowwidth=3,
                arrowcolor='#E2C458',
                arrowsize=1.2,
            ),

            ### force annotation ###
            dict(
                x=mid_pt,
                #x=mid_pt-r_value/2-max_force*conversion,
                y=2,
                text='Force = ' + str(
                    np.format_float_scientific(
                        force(b_value, bo_value, kb_value),
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

fig  = update_bond_force_plot(bond_b_slider.value, bond_bo_slider.value, bond_kb_slider.value)
bond_force_plot = dcc.Graph(id='bond_force_plot',figure=fig)
