import dash_html_components as html
import dash_core_components as dcc
import numpy as np
import plotly.graph_objects as go



lj_text = html.Div([
    html.H2(['Lennard-Jones Potential']),
    html.Hr(),
    html.P([
        '''
        The Lennard-Jones potential is used to describe non-bonded interactions between atoms that arise from van der Waals forces and steric repulsion. The Lennard-Jones potential is defined as:
        '''
    ]),
    html.Div([
        html.Img(src='./assets/images/lj_equation.png',
        style={'height':'50px','filter':'grayscale'}),
        html.P([html.I('where:'),
            html.P([html.Font('\u025B', style={'fontFamily':'serif'}),' = energy constant related to strength of the interaction'], style={'textIndent':'50px'}),
            html.P([html.Font('\u03C3', style={'fontFamily':'serif'}),' = distance constant'], style={'textIndent':'50px'}),
            html.P([html.Font('r', style={'fontFamily':'serif'}),' = distance between atoms'], style={'textIndent':'50px'}),
        ], style={'textAlign':'left', 'lineHeight':0.5}),
    ], style={'textAlign':'center'}),
])


def potential(r, sigma, epsilon):

    """
    returns the Lennard-Jones potential
    """

    lj = 4*epsilon*((sigma/r)**12 - (sigma/r)**6)

    return np.array(lj)

def force(r, sigma, epsilon):

    "returns the force derived from the Lennard-Jones potential"

    lj = -4*epsilon*(sigma**12*(-12)*r**(-13) - sigma**6*(-6)*r**(-7))

    return lj


min_s = 0
max_s = 15
lj_s_slider = dcc.Slider(
    min=min_s,
    max=max_s,
    step=0.1,
    id='lj_s',
    marks={
        min_s: str(min_s),
        max_s: str(max_s),
    },
    value=(max_s - min_s)/2,
    tooltip = { 'always_visible': False },
)

min_r = 1
max_r = 15
lj_r_slider = dcc.Slider(
    min=min_r,
    max=max_r,
    step=0.1,
    id='lj_r',
    marks={
        min_r: str(min_r),
        max_r: str(max_r),
    },
    #value=np.round(1.122*lj_s_slider.value,1),
    value=1,
    tooltip = { 'always_visible': False },
)

min_e = 0
max_e = 1
lj_e_slider = dcc.Slider(
    min=min_e,
    max=max_e,
    step=0.0001,
    id='lj_e',
    marks={
        min_e: str(min_e),
        max_e: str(max_e),
    },
    value=(max_e - min_e)/2,
    tooltip = { 'always_visible': False },
)


### LENNARD-JONES POTENTIAL PLOT ###

if min_r == 0:
    r = np.arange(min_r+0.01,max_r,0.01)
else:
    r = np.arange(min_r,max_r,0.01)
lj = potential(r,lj_s_slider.value,lj_e_slider.value)


# E2C458 yellow
# B09ADB purple
# E6526A pink

#fig = go.Figure()
# fig.add_trace(go.Scatter(x=r, y=lj, mode='lines', line={'color':'#B09ADB','width':5}))
# fig.add_trace(go.Scatter(x=[lj_r_slider.value], y = potential(lj_r_slider.value, lj_s_slider.value, lj_e_slider.value), mode='markers', marker={'color':'#E6526A','size':12}))
# fig.update_xaxes(range=[0,max(r)],showline=True,mirror=True,nticks=5)
# fig.update_yaxes(range=[-max_e*1.5, max_e*3],showline=True,mirror=True,nticks=5)
# fig.update_layout(
#     title='Lennard-Jones Potential',
#     xaxis_title="r",
#     yaxis_title="Potential Energy",
#     font=dict(
#         color="#c3c3c3"
#     ),
#     plot_bgcolor='rgba(0,0,0,0)',
#     paper_bgcolor='rgba(0,0,0,0)',
#     showlegend=False,
# )


def update_lj_plot(e_value, s_value, r_value):

    if min_r == 0:
        r = np.arange(min_r+0.01,max_r,0.01)
    else:
        r = np.arange(min_r,max_r,0.01)
    lj_pot = potential(r,s_value,e_value)

    # E2C458 yellow
    # B09ADB purple
    # E6526A pink

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=r, y=lj_pot, mode='lines', line={'color':'#B09ADB','width':5}))
    fig.add_trace(go.Scatter(x=[r_value], y = potential(r_value, s_value, e_value),
        mode='markers', marker={'color':'#E6526A', 'size':12}))
    fig.update_xaxes(range=[0,max(r)],showline=True,mirror=True,nticks=5)
    fig.update_yaxes(range=[(-max_e)*1.5, max_e*3],showline=True,mirror=True,nticks=5)
    fig.update_layout(
        title='Lennard-Jones Potential',
        xaxis_title="r (\u212B)",
        yaxis_title="Potential Energy (kcal/mol)",
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



def update_lj_force_plot(e_value, s_value, r_value):

    fig = go.Figure()

    # r_range = np.arange(min_r, max_r, 0.0001)
    # lj_pot = potential(r_range, s_value, e_value)
    # mask = np.where(lj_pot <= max_s*3)
    # new_min_r = r_range[mask][0]
    #
    # max_force = force(new_min_r, s_value, e_value)
    # conversion = (max_r)/max_force
    # mid_pt = 2 + max_r
    # current_force = force(r_value, s_value, e_value)
    # if current_force >= max_force:
    #     force_length = max_force*conversion
    # else:
    #     force_length = current_force*conversion
    # print(force_length)

    opt_r = 1.122*s_value
    new_r = r_value - opt_r
    if new_r < 0:
        force_length = -max_r*(-new_r/(opt_r - min_r))
    elif new_r > 0:
        #force_length = (max_r-opt_r)*(new_r/(max_r - opt_r))/2
        force_length = (max_r)*(new_r/(max_r - opt_r))/2
    else:
        force_length = 0
    mid_pt = 2 + max_r



    fig.add_trace(go.Scatter(x=[mid_pt - r_value/2, mid_pt + r_value/2], y = [1.5,1.5],
    mode='markers', hoverinfo='none', marker={'color':'#E6526A', 'size':20}))

    fig.update_xaxes(range=[1,2+1+2*max_r],showline=False,mirror=False,nticks=0,showgrid=False,showticklabels=False)
    fig.update_yaxes(range=[1,2],showline=False,mirror=False,nticks=0,showgrid=False,showticklabels=False)
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(
                x=mid_pt-r_value/2+force_length,
                #x=mid_pt-r_value/2-max_force*conversion,
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
            dict(
                x=mid_pt,
                #x=mid_pt-r_value/2-max_force*conversion,
                y=1.8,
                text='Force = ' + str(np.format_float_scientific(force(r_value, s_value, e_value),precision=2)) + ' kcal/mol',
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
                )
            )
        ],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        font=dict(
            color="#c3c3c3"
        ),
        title='Lennard-Jones Force'
    )

    return fig

fig  = update_lj_force_plot(lj_e_slider.value, lj_s_slider.value, lj_r_slider.value)
lj_force_plot = dcc.Graph(id='lj_force_plot',figure=fig)
