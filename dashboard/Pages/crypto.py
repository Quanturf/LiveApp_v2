# Customized Bullet chart
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


# Raw Package
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr

# Market Data 
import yfinance as yf
import yahoo_fin.stock_info as si

#Graphing/Visualization
import datetime as dt 
import plotly.graph_objs as go 

def make_layout(symbol):

	if symbol is None:
		symbol = 'BTC-USD'

	return html.Div([
		dbc.Card(
			dbc.CardBody([
				dbc.Row([
					dbc.Col([
						drawText()
					], width=2),
					dbc.Col([
						drawText()
					], width=2),
					dbc.Col([
						drawText()
					], width=2),
					dbc.Col([
						drawText()
					], width=2),
					dbc.Col([
						drawText()
					], width=2),
					dbc.Col([
						drawText()
					], width=2),
					
				]), 
				html.Br(),
				dbc.Row([
					dbc.Col([
						centerStock(symbol)
					], width=12),
				], align='center'),      
			]), color = '#15202b' # all cell border
		)
	])



DATATABLE_STYLE = {
    'color': 'white',
    'backgroundColor': '#15202b',
}

DATATABLE_HEADER = {
	'backgroundColor': '#162636',
	'color': 'White',
	'fontWeight': 'bold',
}

TABS_STYLES = {
    'height': '44px'
}
TAB_STYLE = {
    'padding': '15px',
    'fontWeight': 'bold',
	'color': 'white',
	'backgroundColor': '#192734',
	'borderRadius': '10px',
	"margin-left": "6px",
}

TAB_SELECTED_STYLE = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'white',
    'color': '#15202b',
    'padding': '15px',
	'borderRadius': '10px',
	"margin-left": "6px",
}

# Text field
def drawText():
	return html.Div([
		dbc.Card(
			dbc.CardBody([
				html.Div([
					html.H2("Text"),
				], style={'textAlign': 'center', 'color': 'white'}) 
			]), color = '#192734'
		),
	])

def centerStock(symbol):

	ticker = symbol

	# Override Yahoo Finance 
	yf.pdr_override()

	# Retrieve ticker data frame (df) from yfinance API at an interval of 1m 
	df = yf.download(tickers=ticker,period='1d',interval='1m')

		# add Moving Averages (5day and 20day) to df 
	df['MA5'] = df['Close'].rolling(window=5).mean()
	df['MA20'] = df['Close'].rolling(window=20).mean()

	# print(df)

	# Declare plotly figure (go)
	fig=go.Figure()

	fig.add_trace(go.Candlestick(x=df.index,
					open=df['Open'],
					high=df['High'],
					low=df['Low'],
					close=df['Close'], name = 'market data'))

	# Add 5-day Moving Average Trace
	fig.add_trace(go.Scatter(x=df.index, 
							y=df['MA5'], 
							opacity=0.7, 
							line=dict(color='blue', width=2), 
							name='MA 5'))
	# Add 20-day Moving Average Trace
	fig.add_trace(go.Scatter(x=df.index, 
							y=df['MA20'], 
							opacity=0.7, 
							line=dict(color='orange', width=2), 
							name='MA 20'))

	fig.update_xaxes(
		# rangeslider_visible=True,
		rangeselector=dict(
			buttons=list([
				dict(count=15, label="15m", step="minute", stepmode="backward"),
				dict(count=45, label="45m", step="minute", stepmode="backward"),
				dict(count=1, label="HTD", step="hour", stepmode="todate"),
				dict(count=3, label="3h", step="hour", stepmode="backward"),
				dict(step="all")
			]), bgcolor = '#192734'
		)
	)
	fig.update_layout(
		title= str(ticker)+' Live Data:',
		yaxis_title='ticker Price (USD per Shares)',
		template='plotly_dark',
		plot_bgcolor= '#192734',
		paper_bgcolor= '#192734',   
	)

	return html.Div([
			dbc.Card(
				dbc.CardBody([
					dcc.Graph(
						figure=fig,
					config={
						'displayModeBar': False
					}
					)
				]), color = '#192734'
			),  
		])



# def cash_flows(symbol):

# 	ticker = symbol
# 	data = yf.Ticker(ticker)

# 	df = pd.DataFrame(data.cashflow).T
# 	return html.Div([
# 			dbc.Card(
# 				dbc.CardBody([dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
# 								style_data=DATATABLE_STYLE, style_header=DATATABLE_HEADER,style_table={'overflowX': 'auto'})
# 				]), color = '#192734'
# 			),  
# 		])



# def register_callbacks(app):

# 	@app.callback(Output('financials', 'children'), Input('financials-tabs', 'value'), Input('selected-symbol', 'value')
# 	)
# 	def render_financials(tab, symbol):
# 		if tab == 'balance-sheet':
# 			return balance_sheet(symbol)
# 		elif tab == 'income-statement':
# 			return income_statement(symbol)
# 		elif tab == 'cash-flows':
# 			return cash_flows(symbol)

	