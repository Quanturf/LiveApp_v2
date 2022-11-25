import os

# import dash libraries
import dash
from dash import DiskcacheManager, CeleryManager, html, dcc, dash_table
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash.dependencies import Input, Output, State
from datetime import timedelta, datetime, date
import flask

import diskcache

# hosting on heroku
import gunicorn
from whitenoise import WhiteNoise

# import finance libraries
import yfinance as yf
yf.pdr_override()

# import DS libraries
import pandas as pd
import numpy as np
import json

# import files
from dashboard.Pages import home as eq
import dashboard.backtestView as bt_view
import dashboard.LiveTradeView as live_trade
from dashboard.Pages import generate_code as gc
from dashboard.Pages import crypto, fx, equity_visuals, code_modal

PRIMARY = '#FFFFFF'
SECONDARY = '#FFFFFF'
ACCENT = '#98C1D9'
SIDEBAR = '#000000'



asset_class = ''
# get tickers
sp_tickers = pd.read_csv('dashboard/Static/Data/sp500_companies.csv', usecols=['Symbol'])
sp_tickers = sp_tickers['Symbol'].values.tolist()


crypto_tickers = pd.read_csv('dashboard/Static/Data/crypto_tickers.csv', names=['Symbol'])
crypto_tickers = crypto_tickers['Symbol'].values.tolist()

fx_countries = pd.read_csv('dashboard/Static/Data/Foreign_Exchange_Rates.csv')
fx_countries = fx_countries.replace('ND', np.nan) 
fx_countries = fx_countries.dropna()

country_lst = list(fx_countries.columns[2:])

equity_df = pd.DataFrame()

# get all companies from json file
with open('dashboard/Static/Dropdown Data/companies.json', 'r') as read_file:
	company_list = json.load(read_file)
company_options_list = []
for company in company_list:
    company_options_list.append(company)

# set asset specific drowdown values
tickers_dict = {'Equities': company_options_list, 'Crypto': crypto_tickers, 'FX': country_lst, 'Fixed Income': [], 'Commodities': [], 'Sentiment': []}
names = list(tickers_dict.keys())
nested_options = tickers_dict[names[0]]

asset_classes = ['Equities', 'Crypto', 'FX', 'Commodities', 'Fixed Income']
properties = ['Open', 'Low', 'High', 'Volume']

# NEED TO BE CHANGED TO CELERY FOR PRODUCTION
cache = diskcache.Cache('./cache')
background_callback_manager = DiskcacheManager(cache)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], external_scripts=[
    'code.jquery.com/jquery-1.4.2.min.js',
    'cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.5/socket.io.min.js'], 
    suppress_callback_exceptions=True)

server = app.server

server.wsgi_app = WhiteNoise(server.wsgi_app, root='dashboard/Static/')
# server.wsgi_app = WhiteNoise(server.wsgi_app, root='assets/')

eq.register_callbacks(app)
equity_visuals.register_callbacks(app)
bt_view.register_callbacks(app)
#live_trade.register_callbacks(app)
gc.register_callbacks(app)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 54,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'height': '100%',
    'z-index': 1,
    'overflow-x': 'hidden',
    'transition': 'all 0.5s',
    'padding': '0.5rem 1rem',
    'background-color': SIDEBAR, 
	'color': ACCENT,
}

SIDEBAR_HIDEN = {
    'position': 'fixed',
    'top': 54,
    'left': '-16rem',
    'bottom': 0,
    'width': '16rem',
    'height': '100%',
    'z-index': 1,
    'overflow-x': 'hidden',
    'transition': 'all 0.5s',
    'padding': '0rem 0rem',
    'background-color': SIDEBAR,
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    'transition': 'margin-left .5s',
    'margin-left': '16rem',
    'margin-bottom': '30rem',
    'margin-right': 0,
    'padding': '2rem 1rem',
    'background-color': PRIMARY,
}

CONTENT_STYLE1 = {
    'transition': 'margin-left .5s',
    # 'margin-left': '2rem',
    # 'margin-right': '2rem',
    'padding': '2rem 1rem',
    'background-color': PRIMARY,
}
SEARCH_STYLE  = {
    'background-color': PRIMARY,
    'color': 'black',
    }
DATATABLE_STYLE = {
    'color': 'white',
    'backgroundColor': PRIMARY,
}

# Sticky dash board header
navbar = dbc.NavbarSimple(
    children=[
        # dbc.DropdownMenu(
        #     [
        #         dbc.DropdownMenuItem(
        #             "Top Stats", id="headline_stats_df", n_clicks=0
        #         ),
        #         dbc.DropdownMenuItem(
        #             "Equity Timeseries", id="center_stock", n_clicks=0
        #         ),
        #         dbc.DropdownMenuItem(
        #             "Cumulative Returns", id="cumulative_returns_plot", n_clicks=0
        #         ),
        #         dbc.DropdownMenuItem(
        #             "Annual/monthly Returns", id="annual_monthly_returns_plot", n_clicks=0
        #         ),
        #         dbc.DropdownMenuItem(
        #             "Rolling Sharpe", id="rolling_sharpe_plot", n_clicks=0
        #         ),
        #         dbc.DropdownMenuItem(
        #             "Drawdown Underwater", id="drawdown_underwater_plot", n_clicks=0
        #         ),
                
        #     ],
        #     label="Download Data", toggle_style={"color": "white", "backgroundColor": ACCENT, "border":"0"}, style = {"margin-right": "5px"}
        # ),
    
        # dcc.Download(id="download-headline-stats-csv"),
        # dcc.Download(id="download-center-stock-csv"),
        # dcc.Download(id="download-cumulative-returns-csv"),
        # dcc.Download(id="download-anual-monthly-returns-csv"),
        # dcc.Download(id="download-rolling-sharpe-csv"),
        # dcc.Download(id="download-drawdown-underwater-csv"),
        # html.Br(),
        # dbc.Button('Download Data', id="center_stock", n_clicks=0, style = {'color': ACCENT, 'background-color': SIDEBAR, "border-color":ACCENT, "margin-right": "5px"}),
        dbc.Button('See Code', id='open-modal', outline=True, className='mr-1', n_clicks=0, style = {'color': ACCENT, 'background-color': SIDEBAR, "border-color":ACCENT, "margin-right": "5px"}),  
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle('Python Code')),
                dbc.ModalBody(dcc.Markdown(id='see-code-content')),
            ],
            id='modal-content',
            size='lg',
            is_open=False,
            centered=True
        ),
        dbc.Button('Sidebar', outline=True, className='mr-1', id='btn_sidebar', style = {'color': ACCENT, 'background-color': SIDEBAR, "border-color":ACCENT}),
        
    ],
    sticky='top',
    brand='Quanturf - Algo Trading',
    id='navbar',
    brand_href='#',
    color=SIDEBAR,
    dark=True,
    fluid=True,
)
# today = date.today()

# offset = max(1, (today.weekday() + 6) % 7 - 3)
# timedlt1 = timedelta(offset)

# most_recent = today - timedlt1

# offset = max(1, (today.weekday() + 7) % 7 - 3)
# timedlt1 = timedelta(offset)

# second_most_recent = today - timedlt1

# date_object = datetime.strptime(str(most_recent), '%Y-%m-%d %H:%M:%S')
# sidebar, including input for content window
sidebar = html.Div(
    [
        html.Br(),
		
        dbc.Nav(
            [
                html.Br(),
                # dbc.DropdownMenu(label='Equities', children = [dbc.DropdownMenuItem('Visualizations', href='/equity-visuals', id='equity-visuals-link', className='nav-pills'), 
                #                                                 dbc.DropdownMenuItem('Data', href='/backtesting', id='backtesting-link', className='nav-pills'),
                #                                                 ]
                #                 , menu_variant='dark', nav=True, group=True
                # ),
                dbc.NavLink('Download Data', href='/download-data', id='download-data-link', className='nav-pills'),
                dbc.NavLink('Generate Code', href='/generate-code', id='generate-code-link', className='nav-pills'),
                dbc.NavLink('Backtest', href='/backtest', id='backtest-link', className='nav-pills'),
                dbc.NavLink('Live/Paper Trade', href='/live-trade', id='livetrade-link', className='nav-pills'),
                dbc.NavLink('Contact Us', href='/contact-us', id='contact-us-link', className='nav-pills'),
                # dbc.NavLink('Visualizations', href='/equity-visuals', id='equity-visuals-link', className='nav-pills'),
                # dbc.NavLink('Crypto', href='/crypto', id='crypto-link', className='nav-pills'),
                # dbc.NavLink('FX', href='/FX', id='FX-link', className='nav-pills'),
                # dbc.NavLink('Fixed Income', href='/fixed-income', id='fixed-income-link', className='nav-pills'),
                # dbc.NavLink('Commodities', href='/commodities', id='commodities-link', className='nav-pills'),
                # dbc.NavLink('Sentiment', href='/sentiment', id='sentiment-link', className='nav-pills'),
                html.Br(),
                # dcc.DatePickerRange(
                #     id='my-date-picker-range',
                #     min_date_allowed=date(2000, 8, 5),
                #     # max_date_allowed=date(2017, 9, 19),
                #     start_date=second_most_recent,
                #     # initial_visible_month=date(2022, 1, 1),
                #     end_date=most_recent,
                #     style={
                #         'background-color': PRIMARY,
                #         'color': 'black',
                #         'zIndex': 100000
                #     },
                #     calendar_orientation='vertical',
                # ),
                # html.Br(),
                # dcc.Dropdown(asset_classes, 'Equities', id='selected-asset-class', style=SEARCH_STYLE, clearable=False, placeholder='Select Asset Class...'),
                # html.Br(),
                # dcc.Dropdown(value='AAPL', id='selected-symbol', style=SEARCH_STYLE, clearable=False, placeholder='Select Ticker...'),
                # html.Br(),
                # dcc.Dropdown(properties, 'Open', id='selected-property', style=SEARCH_STYLE, clearable=False, placeholder='Select Property...'),
                # html.Br(),
                # dcc.DatePickerRange(
                #     id='my-date-picker-range',
                #     min_date_allowed=date(1995, 8, 5),
                #     max_date_allowed=date.today(),
                #     initial_visible_month=date.today(),
                #     end_date=date.today()
                # ),
                # dmc.DatePicker(
                #     id='start-date',
                #     label='Start Date',
                #     inputFormat='DD-MM-YYYY',
                #     minDate=datetime(1995, 8, 5),
                #     maxDate=datetime.now()- timedelta(1),
                #     value=datetime.now() - timedelta(1),
                #     style=SEARCH_STYLE,
                #     clearable=False
                # ),
                # dmc.DatePicker(
                #     id='end-date',
                #     label='End Date',
                #     inputFormat='DD-MM-YYYY',
                #     minDate=datetime(1995, 8, 5),
                #     maxDate=datetime.now(),
                #     value=datetime.now(),
                #     style=SEARCH_STYLE,
                #     clearable=False
                # ),
                
            ],
            vertical=True,
            pills=True
            
        ),
    ],
    id='sidebar',
    style=SIDEBAR_STYLE,
)


content = html.Div(
	style=CONTENT_STYLE, 
	id='page-content',
	)


app.layout = html.Div([
    dcc.Store(id='side_click'),
    dcc.Location(id='url'),
    navbar,
    sidebar,
    dcc.Loading(
        children=[
            html.Div(
            [
                content,
                
            ], style={'height': '100vh', 'width': '100vw'}
        )],
        type='cube', color = ACCENT
    )], style={'background-color': PRIMARY})
# app.layout = html.Div(
#     [
#         dcc.Store(id='side_click'),
#         dcc.Location(id='url'),
#         navbar,
#         sidebar,
#         content,
#     ]
# )



# toggle see code button in dash header
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

app.callback(
    Output('modal-content', 'is_open'),
    Input('open-modal', 'n_clicks'),
    State('modal-content', 'is_open'),
)(toggle_modal)

categories = ['generate-code', 'download-data','contact-us', 'backtest']





# # adjust dropdown tickers for a given tab
# @app.callback(Output('selected-symbol', 'options'),
#               [Input('selected-asset-class', 'value')]
# )
# def update_dropdown(asset_class):
#     asset_class = asset_class
#     if asset_class == 'Equities':
#         return tickers_dict[asset_class]
#     else:
#         return [{'label': i, 'value': i} for i in tickers_dict[asset_class]]


@app.callback(
    [
        Output('sidebar', 'style'),
        Output('page-content', 'style'),
        Output('side_click', 'data'),
    ],

    [Input('btn_sidebar', 'n_clicks')],
    [
        State('side_click', 'data'),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == 'SHOW':
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = 'HIDDEN'
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = 'SHOW'
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f'{i}-link', 'active') for i in categories],
    [Input('url', 'pathname')],
)
def toggle_active_links(pathname):
    if pathname == '/':
        # Treat page 1 as the homepage / index
        return True, False, False, False
    return [pathname == f'/{i}' for i in categories]

# # communicate with 'see code' content dictionary
# @app.callback(Output('see-code-content', 'children'), [Input('url', 'pathname')])
# def render_code(pathname, symbol):
#     return code_modal.get_modal_content(pathname, symbol)
    
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname in ['/', '/download-data']:
        return eq.make_layout()
    elif pathname == '/backtest':
        return bt_view.make_layout()
    elif pathname =='/generate-code':
        return gc.make_layout()
    elif pathname =='/live-trade':
        return live_trade.make_layout()    
    elif pathname == '/contact-us':
        pass
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        dbc.Container(
            [
                html.H1('404: Not found', className='text-danger'),
                html.Hr(),
                html.P(f'The pathname {pathname} was not recognised...'),
            ],
            fluid=True,
            className='py-3',
        ),
        className='p-3 bg-light rounded-3',
    )

# # @app.callback(Output('nothing', 'children'), Input('url', 'pathname'), background=True, manager=background_callback_manager)
# def get_yf_data():
    
#     for section in range(50, len(company_options_list), 50):
#         # Retrieve stock data frame (df) from yfinance API at an interval of 1m 
#         yf_pd = yf.download(tickers=company_options_list,period='1d',interval='1m', group_by='ticker', auto_adjust = False, prepost = False, threads = True, proxy = None, progress=False)
#         # equity_df.append(df)
#         print('yf', yf_pd)
#         eq.yf_data = pd.concat([yf_pd, eq.yf_data])
#     return html.P(id='placeholder')

    

if __name__ == '__main__':

    app.run_server(debug=True, port=8086)

    
    
    
    