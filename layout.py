from dash import html,dash_table,dcc
import dash_bootstrap_components as dbc

from functions import checkStockCache, grabStockInfo

column_names = ['Stock Name','Ticker','Sector','Industry','# of Shares','Average Cost','Market Price','Day Change %','Dividend/Share','Dividend Yield','Dividend','Gain %','Gain','Total Equity','P/E']

caddata = []
cadsummary =[]
usddata = []
usdsummary =[]
tempdataCAD = checkStockCache('CAD')
print('running first check layout')
for cached in tempdataCAD:
    print(cached)
    stockinfo,summary = grabStockInfo(cached[0],cached[2],cached[3],cached[4])
    tempdict = {column_names[i]:stockinfo[i] for i in range(len(column_names))}
    caddata.append(tempdict)
    cadsummary.append(summary)

#print(caddata)
#print('cadsummary',cadsummary)

if len(caddata) == 0:
    #print('yes')
    caddata = [
    {x:(0) for x in column_names}
    ]


layout = dbc.Container([
    #HEADER SECTION
    # Blue #3459e6
    #Change to more customizable
    dbc.Row([
        #dcc.Interval(id='main-interval',interval=90000)
        dcc.Interval(id={'type':'interval','index':'CAD'},interval=30000),
        dcc.Interval(id={'type':'interval','index':'USD'},interval=30000)
    ]),
    #Nav Bar
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row([
                        dbc.Col(html.Img(src='assets/mainlogo.png', height="30px")),
                        dbc.Col(dbc.NavbarBrand("Stock Scanner", className="ms-2"))],
                        align="center",
                        class_name="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.Row(
                    [
                        dbc.NavbarToggler(id="navbar-toggler"),
                        dbc.Collapse(
                            dbc.Nav(
                                [
                                    dbc.NavItem(dbc.NavLink("Analysis")),
                                    dbc.NavItem(dbc.NavLink("Dashboard")),
                                    dbc.NavItem(
                                        dbc.NavLink("History"),
                                        # add an auto margin after page 2 to
                                        # push later links to end of nav
                                        class_name="me-auto",
                                    ),
                                    dbc.NavItem(dbc.NavLink("Settings")),
                                    dbc.NavItem(dbc.NavLink("Help")),
                                    dbc.NavItem(dbc.NavLink("About")),
                                ],
                                # make sure nav takes up the full width for auto
                                # margin to get applied
                                class_name="w-100",
                            ),
                            id="navbar-collapse",
                            is_open=False,
                            navbar=True,
                        ),
                    ],
                    # the row should expand to fill the available horizontal space
                    class_name="flex-grow-1",
                ),
            ],
            fluid=True,
        ),
        dark=True,
        color="dark",
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
            html.H1(id='total-balance',children=['$0']),
            dbc.DropdownMenu(
                id='currency-label',
                label='CAD',#CHANGE WITH OPTION
                menu_variant="dark",
                children=[
                    dbc.DropdownMenuItem(id={'type':'currency','index':'CAD'},children=['CAD']),
                    dbc.DropdownMenuItem(id={'type':'currency','index':'USD'},children=['USD']),
                    dbc.DropdownMenuItem(id={'type':'currency','index':'GBP'},children=['GBP']),
                    dbc.DropdownMenuItem(id={'type':'currency','index':'EUR'},children=['EUR']),
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
                    label='Canadian Market',
                    id={'type':'tab','index':'CAD'},
                    children=[
                        dbc.Card([
                            dbc.Container([
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
                                                dbc.Col([
                                                    dbc.Label("CAD Value: ")
                                                ],style={'text-align':'right'}),
                                                dbc.Col([
                                                    dbc.Label(id={'type':'value-label','index':'CAD'},children=['0'])
                                                ],style={'text-align':'left'})
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Dropdown(id={'type':'action-dropdown','index':'CAD'},options=['Buy','Sell'],value='Buy',style={'height':'60px'},optionHeight=40)
                                                ]),
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
                                                    dbc.Button('Update Table',id={'type':'stock-confirm','index':'CAD'})
                                                ]),
                                                dbc.Col([]),
                                                dbc.Col([html.H5('Cash:')],style={'text-align':'right'}),
                                                dbc.Col(id={'type':'cash-balance','index':'CAD'},children=[('$1,000')],style={'text-align':'left'}),
                                            ],style={'padding-bottom':'2%'}),
                                            # dbc.Row([
                                            #     dbc.Col([],width=10),
                                            #     dbc.Col([html.H5('Cash:')],style={'text-align':'right'}),
                                            #     dbc.Col([html.H4('$1,000')],style={'text-align':'left'}),
                                            # ]),
                                            #style={'padding-bottom':'2%'})
                                            dbc.Row([
                                                dash_table.DataTable(
                                                    id={'type':'datatable','index':'CAD'},
                                                    columns = [{'name':column,'id':column} for column in column_names],
                                                    data = caddata,
                                                    tooltip_data=[{column_names[0]:x} for x in cadsummary],
                                                    filter_action="native",
                                                    sort_action="native",
                                                    row_selectable="multi",
                                                    style_cell={
                                                        'overflow': 'hidden',
                                                        'textOverflow': 'ellipsis',
                                                        'maxWidth': 0,
                                                    },
                                                )
                                            ],style={'padding-bottom':'4%'}),
                                            # dbc.Row([
                                            #     dbc.Col([html.H5('X-Value')]),
                                            #     dbc.Col([
                                            #         dcc.Dropdown(
                                            #             id='x-val-drop',
                                            #             multi=False,
                                            #             options=column_names
                                            #         )
                                            #     ]),
                                            #     dbc.Col([html.H5('Y-Value')]),
                                            #     dbc.Col([
                                            #         dcc.Dropdown(
                                            #             id='y-val-drop',
                                            #             multi=True,
                                            #             options=column_names
                                            #         )
                                            #     ]),
                                            # ]),
                                            dbc.Row([
                                                dbc.Col(),
                                                dbc.Col(),
                                                dbc.Col(),
                                                dbc.Col([
                                                    dbc.RadioItems(
                                                        id={'type':'graph-radios','index':'CAD'},
                                                        class_name="btn-group",
                                                        inputClassName="btn-check",
                                                        labelClassName="btn btn-outline-primary",
                                                        labelCheckedClassName="active",
                                                        style={'padding':'0%'},
                                                        options=[
                                                            {"label": "1 Day", "value": 1},
                                                            {"label": "5 Day", "value": 2},
                                                            {"label": "1 Month", "value": 3},
                                                            {"label": "3 Month", "value": 4},
                                                            {"label": "1 Year", "value": 5},
                                                        ],
                                                        value=1,
                                                    ),
                                                ]),
                                            ],style={'padding-top':'1%'}),
                                            dbc.Row(id = {'type':'graph-container','index':'CAD'}),
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
                    label='American Market',
                    id={'type':'tab','index':'USD'},
                    children=[
                        dbc.Card([
                            dbc.Container([
                                dbc.Row([
                                    # dbc.Tabs(
                                    #     children=[
                                    #         dbc.Tab(label='Test 1'),
                                    #         dbc.Tab(label='Test 2')
                                    #     ]
                                    html.Center(
                                        dbc.RadioItems(
                                            id={'type':'radioitems','index':'USD'},
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
                                        id={'type':'radio-container','index':'USD'},
                                        children =[
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label("USD Value: ")
                                                ],style={'text-align':'right'}),
                                                dbc.Col([
                                                    dbc.Label(id={'type':'value-label','index':'USD'},children=['0'])
                                                ],style={'text-align':'left'})
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Dropdown(id={'type':'action-dropdown','index':'USD'},options=['Buy','Sell'],value='Buy',style={'height':'60px'},optionHeight=40)
                                                ]),
                                                dbc.Col([
                                                    dbc.FormFloating([
                                                        dbc.Input(id={'type':'stock-input','index':'USD'},type="stock", placeholder="BCE",debounce=True,autoComplete='off',list='suggest-stocks-input'),
                                                        dbc.Label("Stock Name"),
                                                    ])
                                                ]),
                                                dbc.Col([
                                                    dbc.FormFloating([
                                                        dbc.Input(id={'type':'amount-input','index':'USD'},type="number",placeholder='10',min=1,autoComplete='off'),
                                                        dbc.Label("# of Stocks"),
                                                    ])
                                                ]),
                                                dbc.Col([
                                                    dbc.FormFloating([
                                                        dbc.Input(id={'type':'price-input','index':'USD'},type="number",placeholder='20',min=0,autoComplete='off'),
                                                        dbc.Label("$ in USD"),
                                                    ])
                                                ]),
                                                dbc.Col([
                                                    dbc.Button('Update Table',id={'type':'stock-confirm','index':'USD'})
                                                ]),
                                                dbc.Col([]),
                                                dbc.Col([html.H5('Cash:')],style={'text-align':'right'}),
                                                dbc.Col(id={'type':'cash-balance','index':'USD'},children=[('$1,000')],style={'text-align':'left'}),
                                            ],style={'padding-bottom':'2%'}),
                                            # dbc.Row([
                                            #     dbc.Col([],width=10),
                                            #     dbc.Col([html.H5('Cash:')],style={'text-align':'right'}),
                                            #     dbc.Col([html.H4('$1,000')],style={'text-align':'left'}),
                                            # ]),
                                            #style={'padding-bottom':'2%'})
                                            dbc.Row([
                                                dash_table.DataTable(
                                                    id={'type':'datatable','index':'USD'},
                                                    columns = [{'name':column,'id':column} for column in column_names],
                                                    data = usddata,
                                                    tooltip_data=[{column_names[0]:x} for x in usdsummary],
                                                    filter_action="native",
                                                    sort_action="native",
                                                    row_selectable="multi",
                                                    style_cell={
                                                        'overflow': 'hidden',
                                                        'textOverflow': 'ellipsis',
                                                        'maxWidth': 0,
                                                    },
                                                )
                                            ],style={'padding-bottom':'4%'}),
                                            # dbc.Row([
                                            #     dbc.Col([html.H5('X-Value')]),
                                            #     dbc.Col([
                                            #         dcc.Dropdown(
                                            #             id='x-val-drop',
                                            #             multi=False,
                                            #             options=column_names
                                            #         )
                                            #     ]),
                                            #     dbc.Col([html.H5('Y-Value')]),
                                            #     dbc.Col([
                                            #         dcc.Dropdown(
                                            #             id='y-val-drop',
                                            #             multi=True,
                                            #             options=column_names
                                            #         )
                                            #     ]),
                                            # ]),
                                            dbc.Row([
                                                dbc.Col(),
                                                dbc.Col(),
                                                dbc.Col(),
                                                dbc.Col([
                                                    dbc.RadioItems(
                                                        id={'type':'graph-radios','index':'USD'},
                                                        class_name="btn-group",
                                                        inputClassName="btn-check",
                                                        labelClassName="btn btn-outline-primary",
                                                        labelCheckedClassName="active",
                                                        style={'padding':'0%'},
                                                        options=[
                                                            {"label": "1 Day", "value": 1},
                                                            {"label": "5 Day", "value": 2},
                                                            {"label": "1 Month", "value": 3},
                                                            {"label": "3 Month", "value": 4},
                                                            {"label": "1 Year", "value": 5},
                                                        ],
                                                        value=1,
                                                    ),
                                                ]),
                                            ],style={'padding-top':'1%'}),
                                            dbc.Row(id = {'type':'graph-container','index':'USD'}),
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
                    label='Crypto Market',
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

# def MainTab(indexstring):
#     newelement = dbc.Card([
#         dbc.Container([
#             dbc.Row([
#                 # dbc.Tabs(
#                 #     children=[
#                 #         dbc.Tab(label='Test 1'),
#                 #         dbc.Tab(label='Test 2')
#                 #     ]
#                 html.Center(
#                     dbc.RadioItems(
#                         id={'type':'radioitems','index':indexstring},
#                         className="btn-group",
#                         inputClassName="btn-check",
#                         labelClassName="btn btn-outline-primary",
#                         labelCheckedClassName="active",
#                         options=[
#                             {"label": "Dashboard", "value": 1},
#                             {"label": "Watch List", "value": 2},
#                             {"label": "ETF and Market", "value": 3},
#                         ],
#                         value=1,
#                     )
#                 )
#             ],style={'padding-bottom':'2%'}),
#             dbc.Row([
#                 dbc.Container(
#                     id={'type':'radio-container','index':indexstring},
#                     children =[
#                         dbc.Row([
#                             dbc.Col([
#                                 dbc.Label(indexstring + " Value: ")
#                             ],style={'text-align':'right'}),
#                             dbc.Col([
#                                 dbc.Label(id={'type':'value-label','index':indexstring},children=['0'])
#                             ],style={'text-align':'left'})
#                         ]),
#                         dbc.Row([
#                             dbc.Col([
#                                 dcc.Dropdown(id={'type':'action-dropdown','index':indexstring},options=['Buy','Sell'],value='Buy',style={'height':'60px'},optionHeight=40)
#                             ]),
#                             dbc.Col([
#                                 dbc.FormFloating([
#                                     dbc.Input(id={'type':'stock-input','index':indexstring},type="stock", placeholder="BCE",debounce=True,autoComplete='off',list='suggest-stocks-input'),
#                                     dbc.Label("Stock Name"),
#                                 ])
#                             ]),
#                             dbc.Col([
#                                 dbc.FormFloating([
#                                     dbc.Input(id={'type':'amount-input','index':indexstring},type="number",placeholder='10',min=1,autoComplete='off'),
#                                     dbc.Label("# of Stocks"),
#                                 ])
#                             ]),
#                             dbc.Col([
#                                 dbc.FormFloating([
#                                     dbc.Input(id={'type':'price-input','index':indexstring},type="number",placeholder='20',min=0,autoComplete='off'),
#                                     dbc.Label("$ in " + indexstring),
#                                 ])
#                             ]),
#                             dbc.Col([
#                                 dbc.Button('Update Table',id={'type':'stock-confirm','index':indexstring})
#                             ]),
#                             dbc.Col([]),
#                             dbc.Col([html.H5('Cash:')],style={'text-align':'right'}),
#                             dbc.Col(id={'type':'cash-balance','index':indexstring},children=[('$1,000')],style={'text-align':'left'}),
#                         ],style={'padding-bottom':'2%'}),
#                         # dbc.Row([
#                         #     dbc.Col([],width=10),
#                         #     dbc.Col([html.H5('Cash:')],style={'text-align':'right'}),
#                         #     dbc.Col([html.H4('$1,000')],style={'text-align':'left'}),
#                         # ]),
#                         #style={'padding-bottom':'2%'})
#                         dbc.Row([
#                             dash_table.DataTable(
#                                 id={'type':'datatable','index':indexstring},
#                                 columns = [{'name':column,'id':column} for column in column_names],
#                                 data = usddata,
#                                 tooltip_data=[{column_names[0]:x} for x in usdsummary],
#                                 filter_action="native",
#                                 sort_action="native",
#                                 row_selectable="multi",
#                                 style_cell={
#                                     'overflow': 'hidden',
#                                     'textOverflow': 'ellipsis',
#                                     'maxWidth': 0,
#                                 },
#                             )
#                         ],style={'padding-bottom':'4%'}),
#                         # dbc.Row([
#                         #     dbc.Col([html.H5('X-Value')]),
#                         #     dbc.Col([
#                         #         dcc.Dropdown(
#                         #             id='x-val-drop',
#                         #             multi=False,
#                         #             options=column_names
#                         #         )
#                         #     ]),
#                         #     dbc.Col([html.H5('Y-Value')]),
#                         #     dbc.Col([
#                         #         dcc.Dropdown(
#                         #             id='y-val-drop',
#                         #             multi=True,
#                         #             options=column_names
#                         #         )
#                         #     ]),
#                         # ]),
#                         dbc.Row([
#                             dbc.Col(),
#                             dbc.Col(),
#                             dbc.Col(),
#                             dbc.Col([
#                                 dbc.RadioItems(
#                                     id={'type':'graph-radios','index':'USD'},
#                                     class_name="btn-group",
#                                     inputClassName="btn-check",
#                                     labelClassName="btn btn-outline-primary",
#                                     labelCheckedClassName="active",
#                                     style={'padding':'0%'},
#                                     options=[
#                                         {"label": "1 Day", "value": 1},
#                                         {"label": "5 Day", "value": 2},
#                                         {"label": "1 Month", "value": 3},
#                                         {"label": "3 Month", "value": 4},
#                                         {"label": "1 Year", "value": 5},
#                                     ],
#                                     value=1,
#                                 ),
#                             ]),
#                         ],style={'padding-top':'1%'}),
#                         dbc.Row(id = {'type':'graph-container','index':'USD'}),
#                     ]
#                 )
#             ]),
#         ],style={'padding':'2%'})
#     ],style={'margin-top':'1%','padding-top':'1%','padding-bottom':'1%'}),
