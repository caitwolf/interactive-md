import dash_html_components as html

header_text = html.Div([
    html.Div([
        html.H1(['Molecular Dynamics Simulations:'], style={'lineHeight':1}),
        html.H2(['An Interactive Exploration of Atomistic Force Fields'], style={'lineHeight':1}),
        html.P([html.Br()]),
        html.H3(['Caitlyn M. Wolf'], style={'lineHeight':1}),
    ], style={'textAlign':'center', 'lineHeight':0.2}, className = 'column'),
    html.Div([
        html.I([
            'Clean Energy Institute Graduate Fellow 2019-2020',
            html.Br(),
            'Ph.D. Candidate, Department of Chemical Engineering',
            html.Br(),
            'University of Washington, Seattle, WA'
        ])
    ], style={'textAlign':'center'}),
    html.Br(),
])
