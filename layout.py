from dash import html,dash_table,dcc
import dash_bootstrap_components as dbc

column_names = ['Stock Name','Ticker','Sector','Industry','# of Shares','Average Cost','Market Price','Day Change %','Dividend/Share','Dividend Yield','Dividend','Gain %','Gain','Total Equity','P/E']

caddata = [
{x:(0) for x in column_names}
]

layout = dbc.Container([
    #HEADER SECTION
    # Blue #3459e6
    #Change to more customizable
    dbc.Row([
        #dcc.Interval(id='main-interval',interval=90000)
        dcc.Interval(id={'type':'interval','index':'CAD'},interval=30000)
    ]),
    #Nav Bar
    dbc.Navbar(
        dbc.Container([
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='assets/mainlogo.png', height="30px")),
                        dbc.Col(dbc.NavbarBrand("Stock Scanner", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                #SEARCH PART
                [
                    dbc.Row([
                        dbc.Col([
                            html.A(html.H6('History',style={'color':'white'}),href="https://plotly.com",style={"textDecoration": "none"})
                        ]),
                        dbc.Col([
                            html.A(html.H6('Analysis',style={'color':'white'}),href="https://plotly.com",style={"textDecoration": "none"})
                        ]),
                        dbc.Col([
                            html.A(html.H6('Dashboard',style={'color':'white'}),href="https://plotly.com",style={"textDecoration": "none"})
                        ]),
                    ],
                    #className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                    #class_name="w3-padding w3-display-right",
                    #class_name="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                    align="center",
                    style={'margin-left':'auto','margin-right':'0%','text-align':'right'},
                    )
                ],
                id="navbar-collapse",
                is_open=False,
                navbar=True,
                style={}
            ),
        ],style={'margin-left':'2%'}),
    color="dark",
    dark=True,
    #'left':'-12px','right':'0px'
    ),
    # dbc.Row([
    #     dbc.NavbarSimple(
    #         children=[
    #             dbc.NavItem(dbc.NavLink('History',href='history')),
    #             dbc.NavItem(dbc.NavLink('Analysis',href='Analysis')),
    #             dbc.NavItem(dbc.NavLink('Dashboard',href='Dashboard')),
    #         ],
    #         expand='lg',
    #         brand='Stock Scanner',
    #         sticky='top',
    #         brand_href='',
    #         color='primary',
    #         dark=True,
    #     ),
    # ]),
    dbc.Row([html.H5('Portfolio Balance: ')],style={'padding-top':'3%','padding-left':'5%'}),
    dbc.Row([
        dbc.Col([
            html.H1('$100,000'),
            dbc.DropdownMenu(
                label='CAD',#CHANGE WITH OPTION
                children=[
                    dbc.DropdownMenuItem('CAD'),
                    dbc.DropdownMenuItem('USD'),
                    dbc.DropdownMenuItem('GBP'),
                    dbc.DropdownMenuItem('EUR'),
                ],
                size='sm',
                style={'padding-left':'2%','bottom':'-25%'}
            )
        ],style={'display':'flex'}),
        dbc.Col([
            #html.Img(id='conversion-info',src='data:image/png;base64,{}'.format(info_base64),height='20px'),
            html.Img(id='conversion-info',src='assets/info-icon.png',height='20px'),
            dbc.Tooltip(
                children=[
                    html.H5('Test ToolTip',style={'color':'white'})
                ],
                target='conversion-info'
            )
        ],
        width=8),
        #,style={'margin-left':'-25%'}
        dbc.Col([]),
    ],style={'padding-left':'7%'}),
    #],style={'margin-left':'0%'}),
    #Main Body
    dbc.Row([
        dbc.Tabs(
            id='tabs',
            children=[
                dbc.Tab(
                    label='Canadian',
                    children=[
                        dbc.Card([
                            dbc.Container([
                                dbc.Row([
                                    dbc.Col([],width=10),
                                    dbc.Col([html.H5('Cash:')],style={'text-align':'right'}),
                                    dbc.Col([html.H4('$1,000')],style={'text-align':'left'}),
                                ],style={'padding-bottom':'2%'}),
                                dbc.Row([
                                    # dbc.Tabs(
                                    #     children=[
                                    #         dbc.Tab(label='Test 1'),
                                    #         dbc.Tab(label='Test 2')
                                    #     ]
                                    html.Center(
                                        dbc.RadioItems(
                                            id={'type':'radioitems','index':'CAD'},
                                            className="btn-group",
                                            inputClassName="btn-check",
                                            labelClassName="btn btn-outline-primary",
                                            labelCheckedClassName="active",
                                            options=[
                                                {"label": "Dashboard", "value": 1},
                                                {"label": "Watch List", "value": 2},
                                                {"label": "ETF and Market", "value": 3},
                                            ],
                                            value=1,
                                        )
                                    )
                                ],style={'padding-bottom':'2%'}),
                                dbc.Row([
                                    dbc.Container(
                                        id={'type':'radio-container','index':'CAD'},
                                        children =[
                                            dbc.Row([
                                                dbc.Col(['Add to Table:']),
                                                dbc.Col([
                                                    dbc.FormFloating([
                                                        dbc.Input(id={'type':'stock-input','index':'CAD'},type="stock", placeholder="BCE",debounce=True,autoComplete='off',list='suggest-stocks-input'),
                                                        dbc.Label("Stock Name"),
                                                    ])
                                                ]),
                                                dbc.Col([
                                                    dbc.FormFloating([
                                                        dbc.Input(id={'type':'amount-input','index':'CAD'},type="number",placeholder='10',min=1,autoComplete='off'),
                                                        dbc.Label("# of Stocks"),
                                                    ])
                                                ]),
                                                dbc.Col([
                                                    dbc.FormFloating([
                                                        dbc.Input(id={'type':'price-input','index':'CAD'},type="number",placeholder='20',min=0,autoComplete='off'),
                                                        dbc.Label("$ in CAD"),
                                                    ])
                                                ]),
                                                dbc.Col([
                                                    dbc.Button('Confirm',id={'type':'stock-confirm','index':'CAD'})
                                                ]),
                                            ]),
                                            dbc.Row([
                                                dash_table.DataTable(
                                                    id={'type':'datatable','index':'CAD'},
                                                    columns = [{'name':column,'id':column} for column in column_names],
                                                    data = caddata,
                                                    tooltip_data=[],
                                                    filter_action="native",
                                                    sort_action="native",
                                                )
                                            ],style={'padding':'4%'}),
                                            dbc.Row([
                                                dbc.Col([html.H5('X-Value')]),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='x-val-drop',
                                                        multi=False,
                                                        options=column_names
                                                    )
                                                ]),
                                                dbc.Col([html.H5('Y-Value')]),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='y-val-drop',
                                                        multi=True,
                                                        options=column_names
                                                    )
                                                ]),
                                            ]),
                                            dbc.Row([
                                                #px.line()
                                            ]),
                                        ]
                                    )
                                ]),
                            ],style={'padding':'2%'})
                        ],style={'margin-top':'1%','padding-top':'1%','padding-bottom':'1%'}),
                    ],
                    style={'text-align':'center'},
                    tab_style={'margin':'auto'},
                ),
                dbc.Tab(
                    label='American',
                    children=[
                        dbc.Card([
                            html.H4('test')
                        ])
                    ],
                    style={'text-align':'center'},
                    tab_style={'margin':'auto'},
                ),
                dbc.Tab(
                    label='Crypto',
                    children=[
                        dbc.Card([
                            html.H4('test')
                        ])
                    ],
                    style={'text-align':'center'},
                    tab_style={'margin':'auto'},
                )
            ],
            #style={'padding-left':'7%','text-align':'center','margin':'auto'}
        )
    ])
],fluid=True,style={'padding':'0%'})