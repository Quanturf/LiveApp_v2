import warnings
warnings.filterwarnings('ignore')
import os
import tempfile
import zipfile
import uuid

# Customized Bullet chart
import datetime as dt
# import pandas_datareader.data as web
import plotly.express as px
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.express as px
from plotly.tools import mpl_to_plotly
import dash.dependencies
import pyfolio as pf
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import empyrical
import quantstats as qs
from quantstats import stats
from pandas_datareader import data as web
from plotly.subplots import make_subplots


# Raw Package
import numpy as np
import pandas as pd
# from pandas_datareader import data as pdr

# Market Data 
import yfinance as yf
import yahoo_fin.stock_info as si

#Graphing/Visualization
import plotly.graph_objs as go

from re import S
import re
# from turtle import onclick
import redis
import flask

import dashboard.backend as ob
import dashboard.configuration as oc

PRIMARY = '#FFFFFF' 
SECONDARY = '#FFFFFF'
ACCENT = '#98C1D9'
DARK_ACCENT = '#474747'
SIDEBAR = '#F7F7F7'

# global yf_data
# yf_data = pd.DataFrame()
df_dict = {}

debug_mode = False  # set False to deploy

root_directory = os.getcwd()
stylesheets = ['tabs.css']
jss = ['script.js']
static_route = '/Static/'

# level_marks = ['Debug', 'Info', 'Warning', 'Error']
level_marks = {0: 'Debug', 1: 'Info', 2: 'Warning', 3: 'Error'}
num_marks = 4


page = html.Div([
	dbc.Card(
		dbc.CardBody([
			html.Br(),
			dbc.Row([
				dbc.Col([
					# dbc.Card([
					# 	dbc.CardHeader('Download Data', style={'color': DARK_ACCENT}),
					# 	dbc.CardBody([
					# 		# select stocks for backtest + download option
					# 			html.Div([
					# 				dcc.Dropdown(
					# 					id='symbols',
					# 					options=[{'label': name, 'value': name} for name in pd.read_csv('dashboard/Static/sp500_companies.csv')['Symbol'].to_list()],
					# 					#options=['AAPL', 'TSLA', 'MSFT', 'AMZN'], #Replace this with list
					# 					multi=True)
					# 			]),

					# 			html.Br(),

					# 			html.Button('Download', id='download-btn', className='eight columns u-pull-right', n_clicks=0, style={'font-size': '15px', 'font-weight': '5', 'color': PRIMARY, 'background-color': ACCENT, "border-color":ACCENT, 'border-radius': 5}),
					# 	]),
					# ], color=PRIMARY, style={'border-radius': 10}),
					# html.Br(),
					# dbc.Card([
					# 	dbc.CardHeader('Generate Algorithm Code', style={'color': DARK_ACCENT}),
					# 	dbc.CardBody([
					# 			# Generate code
					# 			html.Div([
					# 				html.Div('Algos:', className='four columns'),
					# 				dcc.Dropdown(id='module', options=[], className='eight columns u-pull-right')
					# 				# dcc.Dropdown(
					# 				#     id='module',
					# 				#     options=[{'label': name, 'value': name} for name in oc.cfg['backtest']['modules'].split(',')],
					# 				#     className='eight columns u-pull-right')
					# 			], className='row mb-10'),
					# 			html.Br(),
					# 			html.Div([
					# 				html.Div('Strategy Name:', className='four columns'),
					# 				#dcc.Dropdown(id='strategy', options=[], className='eight columns u-pull-right')
					# 				dcc.Input(id='filename', className='eight columns u-pull-right', value = "MyStrategy", style={'margin-left': '10px', 'width': '210px', 'font-size': '15px', 'font-weight': '5', 'border-radius': 5})
					# 			], className='row mb-10'),

					# 			html.Br(),

					# 			html.Div([
					# 				html.Div('Capital:', className='four columns'),
					# 				#dcc.Dropdown(id='strategy', options=[], className='eight columns u-pull-right')
					# 				dcc.Input(id='cash', className='eight columns u-pull-right', value = 10000, style={'margin-left': '10px', 'width': '210px', 'font-size': '15px', 'font-weight': '5', 'border-radius': 5})
					# 			], className='row mb-10'),
					# 			html.Br(),

					# 			html.Button('Generate Code', id='save-btn', n_clicks=0, className='eight columns u-pull-right', style={'font-size': '15px', 'font-weight': '5', 'color': PRIMARY, 'background-color': ACCENT, "border-color":ACCENT, 'border-radius': 5}),
					# 	]),
					# ], color=PRIMARY, style={'border-radius': 10}),
					#html.Br(),
					dbc.Card([
						dbc.CardHeader('Select Strategy', style={'color': DARK_ACCENT}),
						dbc.CardBody([
								# Run backtest
								html.Div([
									dcc.Dropdown(id='backtest-strategy', options=[], className='eight columns u-pull-right')
									# dcc.Dropdown(
									#     id='module',
									#     options=[{'label': name, 'value': name} for name in oc.cfg['backtest']['modules'].split(',')],
									#     className='eight columns u-pull-right')
								]),
								html.Br(),
								html.Button('Run Backtest', id='backtest-btn', className='eight columns u-pull-right', n_clicks=0, style={'font-size': '15px', 'font-weight': '5', 'color': PRIMARY, 'background-color': ACCENT, "border-color":ACCENT, 'border-radius': 5}),

								html.Div(id='intermediate-value', style={'display': 'none'}),
								html.Div(id='intermediate-params', style={'display': 'none'}),
								html.Div(id='code-generated', style={'display': 'none'}),
								html.Div(id='code-generated2', style={'display': 'none'}),
								# dcc.Download(id="download-data-csv"),
								html.Div(id='intermediate-status', style={'display': 'none'}),
								html.Div(id='level-log', contentEditable='True', style={'display': 'none'}),
								dcc.Input(id='log-uid', type='text', style={'display': 'none'})
							])
					], color = PRIMARY, style ={'border-radius': 10}),
						], width=2),
						dbc.Col([
							
							html.Div([
								dbc.Card(
									dbc.CardBody([
										dbc.Tabs(
											[
												dbc.Tab(dcc.Graph(id='charts',config={
												'displayModeBar': False}), label='Backtest', className='nav-pills'),
												# dbc.Tab(cumulative_returns_plot, label='Cumulative Returns', className='nav-pills'),
												# dbc.Tab(annual_monthly_returns_plot, label='Annual and Monthly Returns', className='nav-pills'),
												# dbc.Tab(rolling_sharpe_plot, label='Rolling Sharpe', className='nav-pills'),
												# dbc.Tab(drawdown_periods_plot, label='unfinished', className='nav-pills'),
												# dbc.Tab(drawdown_underwater_plot, label='Drawdown Underwater', className='nav-pills'),
												# dbc.Tab(quantiles_plot, label='Scatter'),
											],
											id='tabs',
											# active_tab='tab-1',
										),
										
									]), color = SECONDARY, style ={'border-radius': 10}
								),
					]),
				], width=7),

				dbc.Col([
					html.Div([
						dbc.Card(
							dbc.CardBody([
								# html.Div(html.H5('Status'), className='black-block2 mb-10'),  
								# 	html.Div([
								# 		#html.Button('Download', id='download-btn', n_clicks=0, style={'width': '30%', 'margin-left': 0, 'margin-right': '2%'}),
								# 		#html.Button('AutoCode', id='save-btn', n_clicks=0, style={'width': '30%', 'margin-left': 0, 'margin-right': '2%'}),
								# 		#html.Button('Backtest', id='backtest-btn', n_clicks=0, style={'width': '34%', 'margin-left': 0, 'margin-right': '0%'}),
															
								# 	]),
								# 	html.Div(id='status-area', style={
								# 		'margin-top': '10px',
								# 		'padding-left': '10px',
								# 		'border': '1px solid black',
								# 		'line-height': '40px',
								# 		'min-height': '40px',
								# 	}),
								html.Div(id='stat-block')
							]), color = SECONDARY, style ={'border-radius': 10}
						)
					])
				], width=3)
			]),
		])
	)
    ], id='graph-container', style={'margin-bottom':'30rem'}
        # style={'position': 'absolute', 'top': '0px', 'bottom': '0px', 'left': '0px', 'right': '0px'})
)

def make_layout():

	return page






PRIMARY = '#FFFFFF' 
SECONDARY = '#FFFFFF'
ACCENT = '#EF5700'
DARK_ACCENT = '#474747'
SIDEBAR = '#F7F7F7'

# PRIMARY = '#15202b'
# SECONDARY = '#192734'
# ACCENT = '#FFFFFF'
# SIDEBAR = '#F4511E'
#F4511E

DATATABLE_STYLE = {
    'color': 'white',
    'backgroundColor': PRIMARY,
}

DATATABLE_HEADER = {
	'backgroundColor': SIDEBAR,
	'color': 'white',
	'fontWeight': 'bold',
}

TABS_STYLES = {
    'height': '44px'
}
TAB_STYLE = {
    'padding': '15px',
    'fontWeight': 'bold',
	'color': DARK_ACCENT,
	'backgroundColor': SECONDARY,
	'borderRadius': '10px',
	'margin-left': '6px',
}

TAB_SELECTED_STYLE = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': ACCENT,
    'color': PRIMARY,
    'padding': '15px',
	'borderRadius': '10px',
	'margin-left': '6px',
}

# helper function for closing temporary files
def close_tmp_file(tf):
    try:
        os.unlink(tf.name)
        tf.close()
    except:
        pass

# # add csv to download folder
# def add_csv_to_folder(df, name):
# 	filepath = Path('/finailab_dash/Static/download_folder/' + name + '.csv')
# 	filepath.parent.mkdir(parents=True, exist_ok=True)
# 	df.to_csv(filepath)


# @app.callback(Output('backtest-strategy', 'options'), [Input('symbols', 'value')])
# 	def update_algo_list(symbols):

# 		all_files = os.listdir("dashboard/MyStrategies") 
# 		algo_files = list(filter(lambda f: f.endswith('.py'), all_files))
# 		algo_avlb = [s.rsplit( ".", 1 )[ 0 ] for s in algo_files]
# 		#print(algo_avlb)    
# 		return algo_avlb

# Text field
def drawText(title, text):
	return html.Div([
		dbc.Card([
			dbc.CardHeader(title, style={'color': DARK_ACCENT}), 
			dbc.CardBody([
				html.Div([
					# html.Header(title, style={'color': 'white', 'fontSize': 15, 'text-decoration': 'underline', 'textAlign': 'left'}),
					# html.Br(),
					html.Div(str(round(text, 2)), style={'color': DARK_ACCENT, 'textAlign': 'center'}),
					# str(round(text, 2))
				], style={'color': DARK_ACCENT}) 
			])
		], color=PRIMARY, style={'height': 100, 'border-radius': 10}), # , 'backgroundColor':'#FFFFFF', 'border':'1px solid'
	])

def beautify_plotly(fig):
	return html.Div([
			dbc.Card(
				dbc.CardBody([
					dcc.Graph(
						figure=fig,
					config={
						'displayModeBar': False
					}
					)
				]), color = SECONDARY, style ={'border-radius': 10}
			),  
		])

key_metrics_df = pd.DataFrame()
def key_metrics(symbol):
	
	def get_max_drawdown_underwater_f(underwater):
		'''
		Determines peak, valley, and recovery dates given an 'underwater'
		DataFrame.

		An underwater DataFrame is a DataFrame that has precomputed
		rolling drawdown.

		Parameters
		----------
		underwater : pd.Series
		Underwater returns (rolling drawdown) of a strategy.

		Returns
		-------
		peak : datetime
			The maximum drawdown's peak.
		valley : datetime
			The maximum drawdown's valley.
		recovery : datetime
			The maximum drawdown's recovery.
		'''

		#valley = np.argmin(underwater)  # end of the period
		valley = underwater.index[np.argmin(underwater)] # end of the period

		# Find first 0
		peak = underwater[:valley][underwater[:valley] == 0].index[-1]
		# Find last 0
		try:
			recovery = underwater[valley:][underwater[valley:] == 0].index[0]
		except IndexError:
			recovery = np.nan  # drawdown not recovered
		return peak, valley, recovery

	def get_symbol_returns_from_yahoo_f(symbol, start=None, end=None):
		'''
		Wrapper for pandas.io.data.get_data_yahoo().
		Retrieves prices for symbol from yahoo and computes returns
		based on adjusted closing prices.

		Parameters
		----------
		symbol : str
			Symbol name to load, e.g. 'SPY'
		start : pandas.Timestamp compatible, optional
			Start date of time period to retrieve
		end : pandas.Timestamp compatible, optional
			End date of time period to retrieve

		Returns
		-------
		pandas.DataFrame
			Returns of symbol in requested period.
		'''

		try:
			px = web.get_data_yahoo(symbol, start=start, end=end)
			px['date'] = px.index.to_list()
			#px['date'] = px['date'].apply(lambda x: pd.Timestamp(x))
			#px['date'] = pd.to_datetime(px['date'])
			#px['date'] = pd.to_datetime(px['date'], unit='s')
			px.set_index('date', drop=False, inplace=True)
			
			#px.index.rename('date',inplace=True)
			rets = px[['Adj Close']].pct_change().dropna()
			rets.rename(columns={'Adj Close': 'adjclose'},inplace=True)
		except Exception as e:
			warnings.warn(
				'Yahoo Finance read failed: {}, falling back to Google'.format(e),
				UserWarning)
			px = web.get_data_google(symbol, start=start, end=end)
			rets = px[['Close']].pct_change().dropna()

		# rets.index = rets.index.tz_localize('UTC')
		rets.columns = [symbol]
		return rets

	

	empyrical.utils.get_symbol_returns_from_yahoo = get_symbol_returns_from_yahoo_f
	pf.timeseries.get_max_drawdown_underwater = get_max_drawdown_underwater_f
	# return pf.create_returns_tear_sheet(stock_rets)

	stock_rets = pf.utils.get_symbol_rets(symbol)

	# sharpe_ratio = empyrical.sharpe_ratio(stock_rets)
	# max_drawdown = empyrical.max_drawdown(stock_rets)

	def full_report():
		qs.extend_pandas()
		df = pd.DataFrame(stock_rets) 
		df.reset_index(inplace=True)
		# df['date'] = df['date'].apply(pd.to_datetime)
		# report = qs.reports.metrics(stock_rets, mode='full')
		qs.reports.html(stock_rets, output='./assets/full-report.html')
		return html.Div([
			dbc.Card(
				dbc.CardBody(
					# html.Iframe(
					# 	src="~/finailab-dash/quantstats-tearsheet.html",
					# 	# style={"height": "1067px", "width": "100%"},
					# )
					"Coming Soon"
				), color = SECONDARY, style ={'border-radius': 10}
			),  
		])

	def top_stats():
		return [
			stats.kurtosis(stock_rets),
			stats.profit_ratio(stock_rets),
			stats.expected_return(stock_rets),
			stats.exposure(stock_rets),
			stats.tail_ratio(stock_rets),
			stats.value_at_risk(stock_rets),
			stats.payoff_ratio(stock_rets),
			stats.skew(stock_rets),
			stats.win_rate(stock_rets),
			stats.outlier_loss_ratio(stock_rets)
		]

	def cumulative_returns_plot():
		
		# extract data from pyfolio func
		plt = pf.plotting.plot_returns(stock_rets)
		xy_data = plt.get_lines()[0].get_data()
		
		# create plotly fig
		df = pd.DataFrame(xy_data).T
		# add_csv_to_folder(df, "cumulative_returns_plot")
		df_dict['Cumulative Returns'] = df
		fig = px.line(df, x=0, y=1)

		fig.update_layout(
			title= 'Rolling Sharpe Ratio',
			yaxis_title='Returns',
			xaxis_title='Date',
			# template='plotly_dark',
			plot_bgcolor= SECONDARY,
			paper_bgcolor= SECONDARY,
			font=dict(color=DARK_ACCENT)
		)

		return beautify_plotly(fig)
		
	
	def annual_monthly_returns_plot():
		fig = make_subplots(rows=1, cols=3)
		df = pd.DataFrame(stock_rets)
		df['month'] = pd.DatetimeIndex(df.index).month
		df['year'] = pd.DatetimeIndex(df.index).year
		df[symbol] = df[symbol] * 100
		# add_csv_to_folder(df, "annual_monthly_returns_plot")
		df_dict['Annual/monthly Returns'] = df

		fig1 = px.histogram(df, x=symbol)

		fig2 = px.bar(df, x=symbol, y='year', orientation='h')

		fig3 = go.Figure(data=go.Heatmap(
				z=df[symbol],
				x=df['month'],
				y=df['year'],
				colorscale='YlGn'))

		fig = make_subplots(rows=1, cols=3)

		for d in fig1.data:
			fig.add_trace((go.Scatter(x=d['x'], y=d['y'], name = d['name'])), row=1, col=1)
				
		for d in fig2.data:
			fig.add_trace((go.Bar(x=d['x'], y=d['y'],  name = d['name'], orientation='h')), row=1, col=2)

		for d in fig3.data:
			fig.add_trace((go.Heatmap(z=df[symbol], x=df['month'], y=df['year'], colorscale='YlGn')), row=1, col=3)

		fig.update_layout(
			# template='plotly_dark',
			font=dict(color=DARK_ACCENT),
			plot_bgcolor= SECONDARY,
			paper_bgcolor= SECONDARY,
		)

		return beautify_plotly(fig)
	
	# def quantiles_plot():
	# 	fig = pf.plot_return_quantiles(stock_rets)
	# 	return (fig)
	
	def rolling_sharpe_plot():
		fig = pf.plot_rolling_sharpe(stock_rets)
		xy_data = fig.get_lines()[0].get_data()
				
		# create plotly fig
		df = pd.DataFrame(xy_data).T
		# add_csv_to_folder(df, "rolling_sharpe_plot")
		df_dict['Rolling Sharpe'] = df
		fig = px.line(df, x=0, y=1)

		fig.update_layout(
			title= 'Rolling Sharpe Ratio',
			yaxis_title='Sharpe Ratio',
			xaxis_title='Year',
			# template='plotly_dark',
			font=dict(color=DARK_ACCENT),
			plot_bgcolor= SECONDARY,
			paper_bgcolor= SECONDARY,
		)

		return beautify_plotly(fig)

	# NOT FINISHED
	def drawdown_periods_plot():
		fig = pf.plot_drawdown_periods(stock_rets)
		xy_data = fig.get_lines()[0].get_data()
				
		# create plotly fig
		df = pd.DataFrame(xy_data).T
		# add_csv_to_folder(df, "drawdown_periods_plot")
		df_dict['drawdown_periods_plot'] = df
		fig = px.line(df, x=0, y=1)

		fig.update_layout(
			title= 'Top 10 Drawdown Periods',
			yaxis_title='Cumulative Returns',
			xaxis_title='Year',
			# template='plotly_dark',
			font=dict(color=DARK_ACCENT),
			plot_bgcolor= SECONDARY,
			paper_bgcolor= SECONDARY,
		)

		return beautify_plotly(fig)
	
	def drawdown_underwater_plot():
		fig = pf.plot_drawdown_underwater(stock_rets)
		xy_data = fig.get_lines()[0].get_data()
				
		# create plotly fig
		df = pd.DataFrame(xy_data).T
		# add_csv_to_folder(df, "drawdown_underwater_plot")
		df_dict['Drawdown Underwater'] = df
		fig = px.area(df, x=0, y=1)

		fig.update_layout(
			title= 'Underwater Plot',
			yaxis_title='Drawdown',
			xaxis_title='Year',
			# template='plotly_dark',
			font=dict(color=DARK_ACCENT),
			plot_bgcolor= SECONDARY,
			paper_bgcolor= SECONDARY,
		)

		return beautify_plotly(fig)
	return full_report(), top_stats(), cumulative_returns_plot(), annual_monthly_returns_plot(), rolling_sharpe_plot(), drawdown_periods_plot(), drawdown_underwater_plot()




def balance_sheet(symbol):

	ticker = symbol
	data = yf.Ticker(ticker)

	df = pd.DataFrame(data.balance_sheet).T

	return html.Div([
			dbc.Card(
				dbc.CardBody([dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns],
								style_data=DATATABLE_STYLE, style_header=DATATABLE_HEADER, style_table={'overflowX': 'auto'})
				]), color = SECONDARY
			),  
		])

def eps_trend(symbol):

	ticker = symbol
	df = si.get_analysts_info(ticker)['EPS Trend'].assign(hack='').set_index('hack')
	return html.Div([
		dbc.Card(
			dbc.CardBody([dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns],
							style_data=DATATABLE_STYLE, style_header=DATATABLE_HEADER, style_table={'overflowX': 'auto'})
			]), color = SECONDARY
		),  
	])

def growth_estimates(symbol):
	ticker = symbol
	df = si.get_analysts_info(ticker)['Growth Estimates'].assign(hack='').set_index('hack')
	return html.Div([
		dbc.Card(
			dbc.CardBody([dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns],
							style_data=DATATABLE_STYLE, style_header=DATATABLE_HEADER, style_table={'overflowX': 'auto'})
			]), color = SECONDARY
		),  
	])

def earnings_estimate(symbol):
	ticker = symbol
	df = si.get_analysts_info(ticker)['Earnings Estimate'].assign(hack='').set_index('hack')
	return html.Div([
		dbc.Card(
			dbc.CardBody([dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns],
							style_data=DATATABLE_STYLE, style_header=DATATABLE_HEADER, style_table={'overflowX': 'auto'})
			]), color = SECONDARY
		),  
	])
def revenue_estimate(symbol):
	ticker = symbol
	df = si.get_analysts_info(ticker)['Revenue Estimate'].assign(hack='').set_index('hack')
	return html.Div([
		dbc.Card(
			dbc.CardBody([dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns],
							style_data=DATATABLE_STYLE, style_header=DATATABLE_HEADER, style_table={'overflowX': 'auto'})
			]), color = SECONDARY
		),  
	])
def earnings_history(symbol):
	ticker = symbol
	df = si.get_analysts_info(ticker)['Earnings History'].assign(hack='').set_index('hack')
	return html.Div([
		dbc.Card(
			dbc.CardBody([dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns],
							style_data=DATATABLE_STYLE, style_header=DATATABLE_HEADER, style_table={'overflowX': 'auto'})
			]), color = SECONDARY
		),  
	])
def eps_revisions(symbol):
	ticker = symbol
	df = si.get_analysts_info(ticker)['EPS Revisions'].assign(hack='').set_index('hack')
	return html.Div([
		dbc.Card(
			dbc.CardBody([dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns],
							style_data=DATATABLE_STYLE, style_header=DATATABLE_HEADER, style_table={'overflowX': 'auto'})
			]), color = SECONDARY
		),  
	])

def income_statement(symbol):

	ticker = symbol
	data = yf.Ticker(ticker)

	df = pd.DataFrame(data.financials).T
	return html.Div([
			dbc.Card(
				dbc.CardBody([dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns],
								style_data=DATATABLE_STYLE, style_header=DATATABLE_HEADER, style_table={'overflowX': 'auto'})
				]), color = SECONDARY
			),  
		])

def cash_flows(symbol):

	ticker = symbol
	data = yf.Ticker(ticker)

	df = pd.DataFrame(data.cashflow).T
	return html.Div([
			dbc.Card(
				dbc.CardBody([dash_table.DataTable(df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns],
								style_data=DATATABLE_STYLE, style_header=DATATABLE_HEADER,style_table={'overflowX': 'auto'})
				]), color = SECONDARY
			),  
		])


	# @app.callback(Output('financials', 'children'), Input('financials-tabs', 'value'), Input('selected-symbol', 'value')
	# )
	# def render_financials(tab, symbol):

	# 	if symbol is None:
	# 		symbol = 'AAPL'

	# 	if tab == 'balance-sheet':
	# 		return balance_sheet(symbol)
	# 	elif tab == 'income-statement':
	# 		return income_statement(symbol)
	# 	elif tab == 'cash-flows':
	# 		return cash_flows(symbol)
def register_callbacks(app):

	@app.server.route('{}<file>'.format(static_route))
	def serve_file(file):
		if file not in stylesheets and file not in jss:
			raise Exception('"{}" is excluded from the allowed static css files'.format(file))
		static_directory = os.path.join(root_directory, 'Static')
		return flask.send_from_directory(static_directory, file)

	@app.callback(Output('module', 'options'), [Input('symbols', 'value')])
	def update_algo_list(symbols):

		all_files = os.listdir("SampleStrategies") 
		algo_files = list(filter(lambda f: f.endswith('.py'), all_files))
		algo_avlb = [s.rsplit( ".", 1 )[ 0 ] for s in algo_files]
		#print(algo_avlb)    
		return algo_avlb

	# @app.callback(Output('strategy', 'options'), [Input('module', 'value')])
	# def update_strategy_list(module_name):
	#     data = ob.test_list(module_name)
	#     return [{'label': name, 'value': name} for name in data]

	@app.callback(Output('backtest-strategy', 'options'), [Input('symbols', 'value')])
	def update_strategy_list(symbols):  
		print("strat called")
		all_files = os.listdir("dshboard/MyStrategies")    
		backtest_files = list(filter(lambda f: f.endswith('.py'), all_files))
		backtest_avlb = [s.rsplit( ".", 1 )[ 0 ] for s in backtest_files]  
		#print(backtest_avlb) 
		return backtest_avlb

	# I think this callback is not needed. No html tag with id = 'params-table' is there
	# Commenting out it for now.

	# @app.callback(Output('params-table', 'columns'), [Input('module', 'value'), Input('strategy', 'value'), Input('symbols', 'value')])
	# def update_params_list(module_name, strategy_name, symbol):
	#     return ob.params_list(module_name, strategy_name, symbol)


	@app.callback(Output('strategy', 'value'), [Input('strategy', 'options')])
	def update_strategy_value(options):
		if len(options):
			#print(options)
			return options[0]
		return ''


	# @app.callback(Output('status-area', 'children'),
	#               [
	#                   Input('backtest-btn', 'n_clicks'),
	#                   Input('intermediate-params', 'children'),
	#                   Input('intermediate-value', 'children')
	#               ])
	# def update_status_area(n_clicks, packed_params, result):
	#     if result:
	#         return 'Done!'
	#     if n_clicks == 0:
	#         return ''
	#     module, strategy, symbol = None, None, None
	#     try:
	#         params = json.loads(packed_params)
	#         if 'module_i' in params:
	#             module = params['module_i']
	#         if 'strategy_i' in params:
	#             strategy = None if params['strategy_i'] == '' else params['strategy_i']
	#         if 'symbols_i' in params:
	#             symbol = params['symbols_i']
	#     except:
	#         pass
	#     to_provide = []
	#     if module is None:
	#         to_provide.append('module')
	#     if strategy is None:
	#         to_provide.append('strategy')
	#     if symbol is None:
	#         to_provide.append('symbol')
	#     if len(to_provide):
	#         return 'Please provide a value for: {}!'.format(', '.join(to_provide))

	#     return "Backtesting.."


	####  Run Backtest button #####
	
	@app.callback(Output('status-area', 'children'),
				[
					Input('backtest-btn', 'n_clicks'),
					Input('strategy', 'value'),
					Input('intermediate-value', 'children')
				])
	def update_status_area(n_clicks, strategy, result):
		if result:
			return 'Done!'
		if n_clicks == 0:
			return ''
		#strategy = None 
		
		if strategy is None:       
			return 'Please provide a value for: {}!'.format(', '.join(strategy))

		return "Backtesting.."    


	@app.callback(Output('log-uid', 'value'), [Input('symbols', 'options')]) #Why do we need this???
	def create_uid(m):
		return uuid.uuid4().hex


	@app.callback(Output('intermediate-value', 'children'), [Input('strategy', 'value'),Input('backtest-btn', 'n_clicks')])
	def on_click_backtest_to_intermediate(strategy, n_clicks):
		try:
			if strategy is None:
				return []
			#return ob.create_ts(uid, module, strategy, symbols, params)
			result = ob.create_ts2(strategy)
			print("result of backtesting....")
			print(result)
			return result
		except json.decoder.JSONDecodeError:
			# Ignoring this error (this is happening when inputting values in Module/Strategy boxes)
			print("Exception throw ho gya")
			return []    


	# @app.callback(Output('intermediate-value', 'children'),
	#               [Input('intermediate-params', 'children'), Input('log-uid', 'value')])
	# def on_click_backtest_to_intermediate(json_packed, uid):
	#     try:
	#         unpacked = json.loads(json_packed)
	#         module = unpacked['module_i']
	#         strategy = unpacked['strategy_i']
	#         symbols = unpacked['symbols_i']
	#         params = unpacked['table_params']
	#         #params = {}strategy
	#         if module is None or strategy is None or symbols is None:
	#             return []
	#         #return ob.create_ts(uid, module, strategy, symbols, params)
	#         return ob.create_ts2()
	#     except json.decoder.JSONDecodeError:
	#         # Ignoring this error (this is happening when inputting values in Module/Strategy boxes)
	#         return []


	@app.callback(Output('backtest-btn', 'n_clicks'),
				[
					#Input('module', 'value'),
					Input('strategy', 'value')
					#Input('symbols', 'value'),
					#Input('params-table', 'columns')
				])
	def reset_button(*args):
		return 0


	# @app.callback(Output('intermediate-params', 'children'),
	#               [
	#                   Input('backtest-btn', 'n_clicks'),
	#                   Input('module', 'value'),
	#                   Input('strategy', 'value'),
	#                   Input('symbols', 'value')#,
	#                   #Input('params-table', 'columns')
	#               ])
	# def update_params(n_clicks, module, strategy, symbol, rows):
	#     if n_clicks == 0:
	#         return ''
	#     params = {'module_i': module, 'strategy_i': strategy, 'symbols_i': symbol}
	#     table_params = {}
	#     for row in rows:
	#         table_params[row['name']] = str(row['id'])
	#     params['table_params'] = table_params
	#     return json.dumps(params)





	@app.callback(Output('charts', 'figure'),
				[Input('intermediate-value', 'children'), Input('log-uid', 'value')], prevent_initial_call=True)
	def on_intermediate_to_chart(children, uid):
		# r = redis.StrictRedis(oc.cfg['default']['redis'], 6379, db=0)
		# size = r.get(uid + 'size')
		# w, h = size.decode('utf8').split(',')
		# return ob.extract_figure(children, w, h)
		if len(children) == 0:
			return dash.no_update
		return ob.extract_figure(children)

	#Commenting it out for now as there is no level-slider exist.


	@app.callback(Output('stat-block', 'children'), [Input('intermediate-value', 'children')])
	def on_intermediate_to_stat(children):
		statistic = ob.extract_statistic(children)
		ht = []
		for section in statistic:
			ht.append(html.Div(html.B(section, style={'font-size': '1.1em', 'line-height': '1.5m'}), className='row'))
			for stat in statistic[section]:
				ht.append(
					html.Div([
						html.Div(stat, className='u-pull-left'),
						html.Div(html.B(statistic[section].get(stat)), className='u-pull-right')
					], className='row'))
			ht.append(html.Div(style={'border': '1px solid #999', 'margin': '10px 10px 5px'}))
		return html.Div(html.Div(ht[:-1], className='twelve columns', style={'line-height': '1.4em'}), className='row')


	