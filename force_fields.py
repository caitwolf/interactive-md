import dash_html_components as html

ff_text = html.Div([
    html.H2(['Force Fields']),
    html.Hr(),
    html.P([
        '''
        Molecular dynamics force fields are a set of parameters used to define the bonded and non-bonded interactions between atoms in a simulation. A standard equation used to define the potential energy from these interactions in a Class I force field is:
        '''
    ]),

    html.Div([
        html.Img(src='assets/images/ff_equation.png',
        style={'height':'150px'}),
        html.P([html.I('where:'),
            html.P([html.Font('K', style={'fontFamily':'serif'}),' = interaction strength constants'], style={'textIndent':'50px'}),
            html.P([html.Font('b',style={'fontFamily':'serif'}),' = distance between bonded atoms'], style={'textIndent':'50px'}),
            html.P([html.Font('\u03B8',style={'fontFamily':'serif'}),' = angle formed by three bonded atoms'], style={'textIndent':'50px'}),
            html.P([html.Font('\u03B6',style={'fontFamily':'serif'}),' = improper dihedral angle formed by four bonded atoms'], style={'textIndent':'50px'}),
            html.P([html.Font('\u03D5',style={'fontFamily':'serif'}),' = dihedral angle formed by four linearly bonded atoms'], style={'textIndent':'50px'}),
            html.P([html.Font('n',style={'fontFamily':'serif'}),' = integer'], style={'textIndent':'50px'}),
            html.P([html.Font('\u03B4',style={'fontFamily':'serif'}),' = dihedral angle constant for integer n'], style={'textIndent':'50px'}),
            html.P([html.Font('\u025B',style={'fontFamily':'serif'}),' = Lennard-Jones energy constant'], style={'textIndent':'50px'}),
            html.P([html.Font('\u03C3',style={'fontFamily':'serif'}),' = Lennard-Jones distance constant'], style={'textIndent':'50px'}),
            html.P([html.Font('r',style={'fontFamily':'serif'}),' = distance between non-bonded atoms'], style={'textIndent':'50px'}),
            html.P([html.Font('q',style={'fontFamily':'serif'}),' = electronic charge of an atom'], style={'textIndent':'50px'}),
            html.P([html.Font('\u03BA',style={'fontFamily':'sans-serif'}),' = dielectric constant'], style={'textIndent':'50px'}),
        ], style={'textAlign':'left', 'lineHeight':0.5}),
    ], style={'textAlign':'center'}),

    html.Div([
        html.Br(),
        html.P([
            'Force field interaction constants (K) and optimal distances and angles (',
            'b',
            html.Sub('o'),
            ', \u03B8',
            html.Sub('o'),
            ', \u03B6',
            html.Sub('o'),
            '...) are determined by fitting the functional forms in the equation above to the energy of a molecular system at different configurations determined by accurate quantum calculations. In this way, molecular dynamics simulations are able to quickly approximate complex interactions with simplified classical mechanics. There is a cost in accuracy associated with this approach, but it also allows researchers to simulate materials at longer time and length scales with sufficient accuracy in many applications.'
        ]),
    ]),
])
