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

angle_text = html.Div([

    ### header ###
    html.H2(['Angle Potential']),
    html.Hr(),

    html.P([
        '''
        The angle potential (similar to the bond potential) takes the form of a harmonic, similar to that of a spring:
        '''
    ], style={'textAlign':'justify'}),

    ### equation ###
    html.Div([

        html.Img(
            src='./assets/images/angles_equation.png',
            style={
                'height':'50px',
                'filter':'grayscale',
            },
        ),

        html.P([

            html.I('where:'),

            ### th ###
            html.P([

                html.Font('\u03B8', style={'fontFamily':'serif'}),
                ' = angle between three bonded atoms, degrees',

            ], style={'textIndent':'50px'}),

            ### tho ###
            html.P([

                html.Font(['\u03B8', html.Sub('o')], style={'fontFamily':'serif'}),
                ' = angle constant, degrees',

            ], style={'textIndent':'50px'}),

            ### Kth ###
            html.P([

                html.Font(['K', html.Sub('\u03B8')], style={'fontFamily':'serif'}),
                ' = angle constant related to strength of the interaction, energy/degrees', html.Sup('2'),

            ], style={'textIndent':'50px'}),

        ], style={'textAlign':'left', 'lineHeight':0.5}),

    ], style={'textAlign':'center'}),

    html.Br(),

    html.P([
        '''
        The optimal angle between three bonded atoms is found at the bottom of the well in the harmonic angle potential profile. At this point, the force vector is zero. As the two end atoms get closer together, they feel a repulsive (positive) force, and as the atoms get farther away, they feel a proportionally strong attractive force (positive). Similar to the bonded potential, the angle potential is also symmetric. The angle potential energy and force are shown in the graph below. Use the sliders to change the angle between the atoms, as well as the thetao and Ktheta parameters.
        '''
    ], style={'textAlign':'justify'}),

])

### ANGLE INTERACTION FUNCTIONS ###

def potential(th, tho, kth):

    """
    returns the angle potential
    """

    angle_pot = 0.5 * kth * (th-tho)**2
    return np.array(angle_pot)

def force(th, tho, kth):

    "returns the angle force (units N)"

    angle_force = -kth * (th-tho)
    angle_force *= 1e13 # change kj/mol-Ang to N/mol
    return np.array(angle_force)

### tho SLIDER ###

min_tho = 10  # units Angstroms
max_tho = 180 # units Angstroms
angle_tho_slider = dcc.Slider(
    min=min_tho,
    max=max_tho,
    step=1,
    id='angle_tho_slider',
    marks={
        min_tho: str(min_tho),
        max_tho: str(max_tho),
    },
    value=np.round((max_tho-min_tho)/2,1), # starts at optimal distance
    tooltip = { 'always_visible': False },
)

### th SLIDER ###

min_th = 10  # units degrees
max_th = 180 # units degrees
angle_th_slider = dcc.Slider(
    min=min_th,
    max=max_th,
    step=1,
    id='angle_th_slider',
    marks={
        min_th: str(min_th),
        max_th: str(max_th),
    },
    value=np.round(angle_tho_slider.value,0), # starts at optimal distance
    tooltip = { 'always_visible': False },
)

### Kth SLIDER ###

min_kth = 10  # units kJ/mol
max_kth = 100  # units kJ/mol
angle_kth_slider = dcc.Slider(
    min=min_kth,
    max=max_kth,
    step=1,
    id='angle_kth_slider',
    marks={
        min_kth: str(min_kth),
        max_kth: str(max_kth),
    },
    value=np.round((max_kth - min_kth)/2,0),
    tooltip = { 'always_visible': False },
)

### ANGLE POTENTIAL PLOT ###

def update_angle_plot(th_value, tho_value, kth_value):

    th = np.arange(min_th,max_th,0.001)
    if th[0] == 0:
        th = th[1:]

    angle_pot = potential(th, tho_value, kth_value) # kJ/mol
    angle_force = force(th, tho_value, kth_value) # N/mol

    #fig = go.Figure()
    fig = psub.make_subplots(specs=[[{"secondary_y": True}]])

    ### force line ###
    fig.add_trace(
        go.Scatter(
            x=th,
            y=angle_force,
            mode='lines',
            line={'color':'#E2C458','width':5},
        ), secondary_y=True,
    )

    ### potential line ###
    fig.add_trace(
        go.Scatter(
            x=th,
            y=angle_pot,
            mode='lines',
            line={'color':'#B09ADB','width':5},
        )
    )

    ### distance marker ###
    fig.add_trace(
        go.Scatter(
            x=[th_value],
            y = potential(th_value, tho_value, kth_value),
            mode='markers',
            marker={'color':'#E6526A', 'size':12},
        )
    )

    ### distance marker 2 ###
    fig.add_trace(
        go.Scatter(
            x=[th_value],
            y = force(th_value, tho_value, kth_value),
            mode='markers',
            marker={'color':'#E6526A', 'size':12},
        ), secondary_y=True,
    )

    ### graph layout ###
    fig.update_xaxes(
        range=[0,max(th)],
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


    max_pot = potential(min_th, max_tho, max_kth)
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

    max_force = force(min_th, max_tho, max_kth)
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
        title='Angle Potential',
        xaxis_title="\u03B8 (degrees)",
        font=dict(
            color="#c3c3c3"
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
    )

    return fig

fig  = update_angle_plot(angle_th_slider.value, angle_tho_slider.value, angle_kth_slider.value)
angle_plot = dcc.Graph(id='angle_plot',figure=fig)

### ANGLE ATOM-FORCE PLOT ###

def update_angle_force_plot(th_value, tho_value, kth_value):

    theta = np.deg2rad(th_value/2)
    width = np.sin(theta)
    height = np.cos(theta)

    fig = go.Figure()

    top_height = 2.5
    mid_pt = 1 + 0.2 + 1
    mid_pt_height = top_height - height

    ### arc line ###

    radius = 0.3
    arc_height = np.cos(theta)*0.3
    arc_width = np.sin(theta)*0.3
    arc_x = np.arange(mid_pt-arc_width,mid_pt+arc_width,0.001)
    arc_y = top_height - np.sqrt(radius**2 - (arc_x - mid_pt)**2)

    fig.add_trace(
        go.Scatter(
            x=arc_x,
            y=arc_y,
            hoverinfo='none',
            mode='lines',
            line={'color':"#E2C458",'width':2},
        )
    )



    ### atomic markers ###
    fig.add_trace(
        go.Scatter(
            x=[mid_pt, mid_pt - width],
            y=[top_height, mid_pt_height],
            hoverinfo='none',
            mode='lines',
            line={'color':"#c3c3c3",'width':3},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[mid_pt, mid_pt + width],
            y=[top_height, mid_pt_height],
            hoverinfo='none',
            mode='lines',
            line={'color':"#c3c3c3",'width':3},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[mid_pt],
            y = [top_height],
            mode='markers',
            hoverinfo='none',
            marker={'color':'#E6526A', 'size':20}
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[mid_pt - width, mid_pt + width],
            y = [mid_pt_height,mid_pt_height],
            mode='markers',
            hoverinfo='none',
            marker={'color':'#E6526A', 'size':20}
        )
    )


    ### spring ###

    r = 0.1
    tie_len = 0.2

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

    for coil in range(0,5):
        x_step = xplot[-1]
        xplot = np.hstack((xplot,x+x_step))
        yplot = np.hstack((yplot,y))

    x_step = xplot[-1]
    half = int(len(x)/2)+1
    xplot = np.hstack((xplot,x[:half]+x_step))
    yplot = np.hstack((yplot,y[:half]))

    spring_len = 2*width - 2*tie_len
    xplot = tie_len + xplot*spring_len/max(xplot) + mid_pt - 0.5*spring_len - tie_len
    yplot = yplot - r + mid_pt_height

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
            x=[mid_pt-width,mid_pt-width+tie_len],
            y=[mid_pt_height,mid_pt_height],
            hoverinfo='none',
            mode='lines',
            line={'color':"#c3c3c3",'width':3},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[mid_pt+width,mid_pt+width-tie_len],
            y=[mid_pt_height,mid_pt_height],
            hoverinfo='none',
            mode='lines',
            line={'color':"#c3c3c3",'width':3},
        )
    )

    ### graph layout ###
    fig.update_xaxes(
        range=[1,1+0.2+1+1+0.2],
        showline=False,
        mirror=False,
        nticks=0,
        showgrid=False,
        showticklabels=False,
    )

    fig.update_yaxes(
        range=[1.3,2.7],
        showline=False,
        mirror=False,
        nticks=0,
        showgrid=False,
        showticklabels=False,
    )

    max_force = force(max_th, min_tho, kth_value)
    conversion = 1/(1.1*max_force)
    force_length = force(th_value, tho_value, kth_value)*conversion

    if force_length < 0:
        theta2 = np.arctan(height/width)
        theta3 = np.deg2rad(90) - theta2
        width2 = -1*np.cos(theta3)*np.abs(force_length)
        height2 = -1*np.sin(theta3)*np.abs(force_length)

    elif force_length > 0 :
        theta2 = np.arctan(height/width)
        theta3 = theta2
        width2 = np.sin(theta3)*np.abs(force_length)
        height2 = np.cos(theta3)*np.abs(force_length)

    else:
        width2 = 0
        height2 = 0



    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=280,
        width=2.4*280/1.4,
        font=dict(
            color="#c3c3c3",
        ),
        title='Angle Interaction',
        #autosize=False,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=2
        ),
        annotations=[

            ### theta annotation ###
            dict(
                x=mid_pt,
                #x=mid_pt-r_value/2-max_force*conversion,
                y=2,
                text='\u03B8',
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

            ### left force vector ###
            dict(
                x=mid_pt-width+width2,
                y=mid_pt_height-height2,
                xref="x",
                yref="y",
                showarrow=True,
                arrowhead=1,
                axref="x",
                ayref="y",
                ax=mid_pt-width,
                ay=mid_pt_height,
                arrowwidth=3,
                arrowcolor='#E2C458',
                arrowsize=1.2,
            ),

            ### right force vector ###
            dict(
                x=mid_pt+width-width2,
                y=mid_pt_height-height2,
                xref="x",
                yref="y",
                showarrow=True,
                arrowhead=1,
                axref="x",
                ayref="y",
                ax=mid_pt+width,
                ay=mid_pt_height,
                arrowwidth=3,
                arrowcolor='#E2C458',
                arrowsize=1.2,
            ),

            ### force annotation ###
            dict(
                x=mid_pt,
                #x=mid_pt-r_value/2-max_force*conversion,
                y=top_height-1.2,
                text='Force = ' + str(
                    np.format_float_scientific(
                        force(th_value, tho_value, kth_value),
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

fig  = update_angle_force_plot(angle_th_slider.value, angle_tho_slider.value, angle_kth_slider.value)
angle_force_plot = dcc.Graph(id='angle_force_plot',figure=fig)
