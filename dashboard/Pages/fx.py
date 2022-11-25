# # Customized Bullet chart
# import datetime as dt
# import pandas_datareader.data as web
# import plotly.express as px
# from dash import html, dcc, dash_table
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output


# import datetime
# import requests

# # Raw Package
# import numpy as np
# import pandas as pd
# from pandas_datareader import data as pdr

# # Market Data 
# import yfinance as yf
# import yahoo_fin.stock_info as si

# #Graphing/Visualization
# import datetime as dt 
# import plotly.graph_objs as go 

# def make_layout(symbol):

# 	if symbol is None:
# 		symbol = 'EURO AREA - EURO/US$'

# 	return html.Div([
# 		dbc.Card(
# 			dbc.CardBody([
# 				dbc.Row([
# 					dbc.Col([
# 						update_news()
# 					], width=3),
# 					dbc.Col([
# 						main_graph(symbol)
# 					], width=9),
# 				], align='center'),      
# 			html.Br(),
	
# 			]), color = PRIMARY, style ={'border-radius': 10} # all cell border
# 		)
# 	], style={'margin-bottom':'30rem'})

# PRIMARY = '#FFFFFF'
# SECONDARY = '#FFFFFF'

# DATATABLE_STYLE = {
#     'color': 'white',
#     'backgroundColor': '#15202b',
# }

# DATATABLE_HEADER = {
# 	'backgroundColor': '#162636',
# 	'color': 'White',
# 	'fontWeight': 'bold',
# }

# LINK_TABLE_HEADER = {
# 	'color': 'white',
# 	'backgroundColor': '#192734',
# 	'fontSize': '12px',
# }

# LINK_TABLE = {
# 	'color': 'white',
# 	'backgroundColor': '#192734'
# }

# TABS_STYLES = {
#     'height': '44px'
# }
# TAB_STYLE = {
#     'padding': '15px',
#     'fontWeight': 'bold',
# 	'color': 'white',
# 	'backgroundColor': '#192734',
# 	'borderRadius': '10px',
# 	"margin-left": "6px",
# }

# TAB_SELECTED_STYLE = {
#     'borderTop': '1px solid #d6d6d6',
#     'borderBottom': '1px solid #d6d6d6',
#     'backgroundColor': 'white',
#     'color': '#15202b',
#     'padding': '15px',
# 	'borderRadius': '10px',
# 	"margin-left": "6px",
# }

# # Text field
# def drawText():
# 	return html.Div([
# 		dbc.Card(
# 			dbc.CardBody([
# 				html.Div([
# 					html.H2("Text"),
# 				], style={'textAlign': 'center', 'color': 'white'}) 
# 			]), color = '#192734'
# 		),
# 	])
	
# # Currency pairs
# currencies = ["EURUSD", "USDCHF", "USDJPY", "GBPUSD"]

# # API Requests for news div
# news_requests = requests.get(
#     "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=da8e2e705b914f9f86ed2e9692e66012"
# )

# # API Call to update news
# def update_news():
#     json_data = news_requests.json()["articles"]
#     df = pd.DataFrame(json_data)
#     df = pd.DataFrame(df[["title", "url"]])
#     max_rows = 10
#     return html.Div([
# 			dbc.Card(
# 				dbc.CardBody([
# 					html.P(className="p-news", children="Headlines", style={'fontSize':'30px', 'fontWeight':'Medium'}),
# 					html.P(
# 						className="p-news float-right",
# 						children="Last update : "
# 						+ datetime.datetime.now().strftime("%H:%M:%S"),
# 						# style=LINK_TABLE_HEADER
# 					),
# 					html.Table(
# 						className="table-news",
# 						children=[
# 							html.Tr(
# 								children=[
# 									html.Td(
# 										children=[
# 											html.A(
# 												className="td-link",
# 												children=df.iloc[i]["title"],
# 												href=df.iloc[i]["url"],
# 												target="_blank"
# 											)
# 										]
# 									)
# 								]
# 							)
# 							for i in range(min(len(df), max_rows))
# 						],
# 					),
# 				]), color = SECONDARY, style ={'border-radius': 10}
# 			),
#         ]
#     )

# def main_graph(countries):

# 	data = pd.read_csv('Static/Data/Foreign_Exchange_Rates.csv')
# 	data= data.replace('ND', np.nan) 
# 	data = data.dropna()

# 	country_lst = list(data.columns[2:])
# 	colour_lst = ['#91930b', '#6cdc93', '#935049', '#acbc09', '#0b92d3', '#dc8845', '#a60c7c', '#4a31f7', '#d8191c', '#e86f71','#efd4f3','#2e0e88','#7d4c26','#0bc039','#fa378c','#54f1e5','#7a0a8b','#43142d','#beaef4','#04b919','#91dde5','#2a850d']

# 	color_dict = dict(zip(country_lst, colour_lst))
# 	# Initialise figure 
# 	fig = go.Figure()
# 	fig.update_yaxes(automargin=True)

# 	# Add Traces
# 	fig.add_trace(
# 		go.Scatter(x= data['Time Serie'],
# 						y= data[countries],
# 						line=dict(color=color_dict[countries]))
# 	)

# 	fig.update_layout(
# 		title=countries,
# 		# template='plotly_dark',
# 		# plot_bgcolor= '#192734',
# 		# paper_bgcolor= '#192734',   
# 	)
# 	fig.update_yaxes(categoryorder='category ascending')

# 	return html.Div([
# 			dbc.Card(
# 				dbc.CardBody([
# 					dcc.Graph(
# 						figure=fig,
# 					config={
# 						'displayModeBar': False
# 					}
# 					)
# 				]), color = SECONDARY, style ={'border-radius': 10}
# 			),  
# 		])