import warnings
warnings.filterwarnings('ignore')
import os
import tempfile
import zipfile

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

# global yf_data
# yf_data = pd.DataFrame()
df_dict = {}

def make_layout():

	# if symbol is None:
	symbol = 'AAPL'
		# app.equity_df.append(yf.download(tickers='AAPL',period='1d',interval='1m', group_by='ticker', auto_adjust = False, prepost = False, threads = True, proxy = None))
	# full_report, top_stats, cumulative_returns_plot, annual_monthly_returns_plot, rolling_sharpe_plot, drawdown_periods_plot, drawdown_underwater_plot = key_metrics(symbol)
	top_stats, cumulative_returns_plot, annual_monthly_returns_plot, rolling_sharpe_plot= key_metrics(symbol)
	kurtosis, profit_ratio, expected_return, exposure, tail_ratio, value_at_risk, payoff_ratio, skew, win_rate, outlier_loss_ratio = top_stats
	headline_stats_df = pd.DataFrame.from_dict({'kurtosis': [kurtosis], 'profit_ratio': [profit_ratio], 'expected_return': [expected_return], 
			'exposure':[exposure], 'tail_ratio':[tail_ratio], 'value_at_risk':[value_at_risk], 'payoff_ratio':[payoff_ratio],
			 'skew':[skew], 'win_rate':[win_rate], 'outlier_loss_ratio':[outlier_loss_ratio]})
	df_dict['Top Stats'] = headline_stats_df

	return html.Div([
		dbc.Col([					
					dbc.Card([
						dbc.CardHeader('Select Strategy', style={'color': DARK_ACCENT}),
						dbc.CardBody([
								# Run backtest
								html.Div([
									dcc.Dropdown(
										id='backtest-strategy', 
										options=[s.rsplit( ".", 1 )[ 0 ] for s in list(filter(lambda f: f.endswith('.py'), os.listdir("dashboard/MyStrategies")))],
									)
									#backtest_avlb = 
									# dcc.Dropdown(
									#     id='module',
									#     options=[{'label': name, 'value': name} for name in oc.cfg['backtest']['modules'].split(',')],
									#     className='eight columns u-pull-right')
								]),

								html.Br(),
								dbc.Row([
									#html.Br(),
										dbc.Col([
											html.Button('Live Trade', id='backtest-btn', className='eight columns u-pull-right', n_clicks=0, style={'font-size': '15px', 'font-weight': '5', 'color': PRIMARY, 'background-color': ACCENT, "border-color":ACCENT, 'border-radius': 5}),
										]),
									html.Br(),

									dbc.Col([
										html.Button('Cloud Deploy', id='backtest-btn', className='eight columns u-pull-right', n_clicks=0, style={'font-size': '15px', 'font-weight': '5', 'color': PRIMARY, 'background-color': ACCENT, "border-color":ACCENT, 'border-radius': 5}),
									]),
								]),
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
						], width=3),
		dbc.Card(
			dbc.CardBody([
				dbc.Row([
					dbc.Col([
						drawText('Dollar PnL', kurtosis)
					]),
					dbc.Col([
						drawText('Return', profit_ratio)
					]),

					dbc.Col([
						drawText('Realized PL', exposure)
					]),
					dbc.Col([
						drawText('Unrealized PL', tail_ratio)
					]),
					dbc.Col([
						drawText('Total Val.', value_at_risk)
					]),
					dbc.Col([
						drawText('Max DD', payoff_ratio)
					]),
					dbc.Col([
						drawText('Aval. Cash', skew)
					]),
					dbc.Col([
						drawText('Win Rate', win_rate)
					]),
					# dbc.Col([
					# 	drawText('Outlier loss Ratio', outlier_loss_ratio)
					# ]),
					
				]), 
				html.Br(),
				dbc.Row([
					# dbc.Col([
					# 	eps_trend(symbol),
					# 	eps_revisions(symbol)
					# ], width=3),
					dbc.Col([
						dbc.Tabs(
					[
						dbc.Tab(cumulative_returns_plot, label='Performance', className='nav-pills'),
						dbc.Tab(annual_monthly_returns_plot, label='Closed Position', className='nav-pills'),
						dbc.Tab(rolling_sharpe_plot, label='Open Positions', className='nav-pills'),
						#dbc.Tab(drawdown_periods_plot, label='unfinished', className='nav-pills'),
						#dbc.Tab(drawdown_underwater_plot, label='Drawdown Underwater', className='nav-pills'),
						# dbc.Tab(quantiles_plot, label='Scatter'),
					],
					id='tabs',
					# active_tab='tab-1',
					# active_tab='tab-1',
				),
					], width=9),
					dbc.Col([
						#full_report
					], width=3),
				], align='center'), 
				html.Br(),
				
     
			]), color = PRIMARY, style ={'border-radius': 10} # all cell border
		)
	], style={'margin-bottom':'30rem'})





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

# Text field
def drawText(title, text):
	return html.Div([
		dbc.Card([
			dbc.CardHeader(title, style={'color': DARK_ACCENT}), 
			dbc.CardBody([
				html.Div([
					# html.Header(title, style={'color': 'white', 'fontSize': 15, 'text-decoration': 'underline', 'textAlign': 'left'}),
					# html.Br(),
					html.Div(str(round(text, 2)), style={'color': DARK_ACCENT, 'textAlign': 'left'}),
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
			#px = web.get_data_yahoo(symbol, start=start, end=end)
			data_dir = "dashboard/Data/"  
			px = pd.read_csv(os.path.join(data_dir, symbol+".csv"), parse_dates=True)
			px['date'] = px.index.to_list()
			#px['date'] = px['date'].apply(lambda x: pd.Timestamp(x))
			#px['date'] = pd.to_datetime(px['date'])
			#px['date'] = pd.to_datetime(px['date'], unit='s')
			px.set_index('date', drop=False, inplace=True)
			
			#px.index.rename('date',inplace=True)
			rets = px[['Close']].pct_change().dropna()
			rets.rename(columns={'Close': 'adjclose'},inplace=True)
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
	# return full_report(), top_stats(), cumulative_returns_plot(), annual_monthly_returns_plot(), rolling_sharpe_plot(), drawdown_periods_plot(), drawdown_underwater_plot()
	return  top_stats(), cumulative_returns_plot(), annual_monthly_returns_plot(), rolling_sharpe_plot()	



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
