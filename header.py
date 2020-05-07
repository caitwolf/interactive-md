import dash_html_components as html

header_text = html.Div([

    html.Div([
        html.H1(['Molecular Dynamics Simulations:'], style={'lineHeight':1}),
        html.H1([html.I('An Interactive Exploration of Atomistic Force Fields')], style={'lineHeight':1}),
    ], style={'textAlign':'center', 'lineHeight':1}, className = 'column'),

    html.Div([

        html.Div([
            html.Div([
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
        ], className = 'col-sm-6'),
        
        html.Div([
            html.A([
                html.Img(src='assets/images/cei-logo-white.png', style={'width':'300px'})
            ], href='https://www.cei.washington.edu/', style={'textAlign':'center'}),
        ], className='col-sm-6', style={'verticalAlign':'center', 'paddingTop':'25px'}),

    ], className='row')
],)

# header_text = html.Div([
#     html.Div([
#         'test'
#     ], className='')
# ], className='row')
