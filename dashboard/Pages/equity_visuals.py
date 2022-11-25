import FundamentalAnalysis as fa
import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import json
import yfinance as yf


TITLE_STYLE = {
		'color': 'white',
		'backgroundColor': '#15202b',
	}
GRAPH_STYLE = {
	'color': 'white',
	'background-color': '#192734',
	
}

SEARCH_STYLE  = {
	"background-color": "#15202b",
	'color': 'black',
	}
def create_drop_down_options(json_file, dictionary=True):
	with open("dashboard/Static/Dropdown Data/" + json_file, "r") as read_file:
		data = json.load(read_file)

	output = []
	if dictionary is True:
		for item in data:
			output.append({'label': item, 'value': data[item]})
	else:
		for item in data:
			output.append({'label': item, 'value': item})

	return output

with open("dashboard/Static/Dropdown Data/companies.json", "r") as read_file:
	company_list = json.load(read_file)
company_options_list = []
for company in company_list:
	company_options_list.append({'label': str(company_list[company] + ' (' + company + ')'),
								'value': company})

# with open("dashbord/Static/Dropdown Data/sector_per_company.json", "r") as read_file:
# 	sector_per_company = json.load(read_file)

with open("dashboard/Static/Dropdown Data/industry_per_company.json", "r") as read_file:
	industry_per_company = json.load(read_file)

sectors_options_list = create_drop_down_options("sectors.json", dictionary=False)
industries_options_list = create_drop_down_options("industries.json", dictionary=False)
key_metrics_options_list = create_drop_down_options("key_metrics.json")
ratios_options_list = create_drop_down_options("financial_ratios.json")
balance_sheet_statement_options = create_drop_down_options("balance_sheet_statement.json", dictionary=False)
income_statement_options = create_drop_down_options("income_statement.json", dictionary=False)
cash_flow_statement_options = create_drop_down_options("cash_flow_statement.json", dictionary=False)
financial_statement_growth_options = create_drop_down_options("financial_statement_growth.json", dictionary=False)


def make_layout():

	return html.Div([
			dbc.Card(
			dbc.CardBody([
				dbc.Row([
					dbc.Col([
						html.Summary('API Key', style=TITLE_STYLE),
						dcc.Input(
							id="api", style={'width': '100%'})
					], width=2),
					dbc.Col([
						html.Summary('Sectors', style=TITLE_STYLE),
						dcc.Dropdown(
							id="sectors",
							options=sectors_options_list,
							multi=True, style=SEARCH_STYLE, optionHeight=60)
					], width=2),
					dbc.Col([
						html.Summary('Companies', style=TITLE_STYLE),
						dcc.Dropdown(
							id="companies",
							options=company_options_list,
							multi=True, style=SEARCH_STYLE, optionHeight=60)
						
					], width=2),
					dbc.Col([
						html.Summary('Financial Ratios', style=TITLE_STYLE),
						dcc.Dropdown(
							id="financial_ratios",
							options=ratios_options_list,
							multi=True, style=SEARCH_STYLE, optionHeight=60)
					], width=2),
					dbc.Col([
						html.Div([
							html.Div([
								html.Summary('Period',
											style={'padding-right': "10px", 'color': 'white'}),
								dcc.RadioItems(
									id='period',
									value='annual',
									options=[
										{'label': 'Annually', 'value': 'annual'},
										{'label': 'Quarterly', 'value': 'quarter'}],
									labelStyle={'display': 'inline-block', 'padding-right': '5px'})
							], style={'display': 'flex', "padding-top": "10px", 'color': 'white'}),

							html.Div([
								html.Summary('Data',
											style={'padding-right': "20px", 'color': 'white'}),
								dcc.RadioItems(
									id='data_type',
									value='linear',
									options=[
										{'label': 'Linear', 'value': 'linear'},
										{'label': 'Log', 'value': 'log'}],
									labelStyle={'display': 'inline-block', 'padding-right': '5px'})
							], style={'display': 'flex', "padding-bottom": "10px",
									'border-bottom': '1px solid #ffeedd', 'color': 'white'})
					])
					], width=2),
					dbc.Col([
						html.Summary('Key Metrics', style=TITLE_STYLE),
						dcc.Dropdown(
							id="key_metrics",
							options=key_metrics_options_list,
							multi=True, style=SEARCH_STYLE, optionHeight=60)
					], width=2),
					
				]), 
				dbc.Row([
					dbc.Col([
						dbc.Button(
							"See Company Profiles", id="open-body-scroll", n_clicks=0, outline=True, color='secondary', style={'width':'15.4rem'}
						),
						dbc.Modal(
							[
								
								dbc.ModalBody(id="company_profile_container", style={'padding': '3rem'}),
								html.Div(id='company_profile_data', style={'display': 'none', 'padding': '3rem'}),
								
								dbc.ModalFooter(
									dbc.Button(
										"Close",
										id="close-body-scroll",
										className="ms-auto",
										n_clicks=0,
										color='secondary',
										outline=True
									)
								),
							],
							id="modal-body-scroll",
							scrollable=True,
							is_open=False,
							size="lg",
						),
						
					], width=2),
					dbc.Col([
						html.Summary('Industries', style=TITLE_STYLE),
						dcc.Dropdown(
							id="industries",
							options=industries_options_list,
							multi=True, style=SEARCH_STYLE, optionHeight=60)
					], width=2),
					dbc.Col([
						html.Summary('Balance Sheet Statement', style=TITLE_STYLE),
						dcc.Dropdown(
							id="balance_sheet_statement",
							options=balance_sheet_statement_options,
							multi=True, style=SEARCH_STYLE, optionHeight=60)
					], width=2),
					dbc.Col([
						html.Summary('Cash Flow Statement', style=TITLE_STYLE),
						dcc.Dropdown(
							id="cash_flow_statement",
							options=cash_flow_statement_options,
							multi=True, style=SEARCH_STYLE, optionHeight=60)
					], width=2),
					dbc.Col([
						html.Summary('Income Statement', style=TITLE_STYLE),
						dcc.Dropdown(
							id="income_statement",
							options=income_statement_options,
							multi=True, style=SEARCH_STYLE, optionHeight=60)
					], width=2),
					dbc.Col([
						html.Summary('Financial Statement Growth', style=TITLE_STYLE),
						dcc.Dropdown(
							id="financial_statement_growth",
							options=financial_statement_growth_options,
							multi=True, style=SEARCH_STYLE, optionHeight=60)
					], width=2),
					
				]),
				html.Br(),

				dbc.Row([

					html.Div(id="stock_data_container",style={'padding-bottom': '2rem', 'width': '45%', 'display': 'inline-block none'}),
					html.Div(id="key_metrics_container", style={'padding-bottom': '2rem', 'width': '45%', 'display': 'inline-block'}),
					html.Div(id="ratios_container", style={'padding-bottom': '2rem', 'width': '45%', 'display': 'inline-block'}),
					html.Div(id="balance_sheet_container", style={'padding-bottom': '2rem', 'width': '45%', 'display': 'inline-block'}),
					html.Div(id="income_statement_container", style={'padding-bottom': '2rem', 'width': '45%', 'display': 'inline-block'}),
					html.Div(id="cash_flow_statement_container", style={'padding-bottom': '2rem', 'width': '45%', 'display': 'inline-block'}),
					html.Div(id="financial_statement_growth_container", style={'padding-bottom': '2rem', 'width': '45%', 'display': 'inline-block'}),

					html.Div(id='stock_data', style={'padding-bottom': '2rem', 'width': '45%', 'display': 'none'}),
					html.Div(id='key_metrics_data', style={'padding-bottom': '2rem', 'width': '45%', 'display': 'none'}),
					html.Div(id='ratios_data', style={'padding-bottom': '2rem', 'width': '45%', 'display': 'none'}),
					html.Div(id='balance_sheet_data', style={'padding-bottom': '2rem', 'width': '45%', 'display': 'none'}),
					html.Div(id='income_statement_data', style={'padding-bottom': '2rem', 'width': '45%', 'display': 'none'}),
					html.Div(id='cash_flow_statement_data', style={'padding-bottom': '2rem', 'width': '45%', 'display': 'none'}),
					html.Div(id='financial_statement_growth_data', style={'padding-bottom': '2rem', 'width': '49%', 'display': 'none'}),
					
				]),
			]), color = '#15202b'
			)
	], style={'margin-bottom':'35rem'})


def register_callbacks(app):

	@app.callback(
		Output("modal-body-scroll", "is_open"),
		[
			Input("open-body-scroll", "n_clicks"),
			Input("close-body-scroll", "n_clicks"),
		],
		[State("modal-body-scroll", "is_open")],
	)
	def toggle_modal(n1, n2, is_open):
		if n1 or n2:
			return not is_open
		return is_open

	@app.callback(
		Output(component_id='companies', component_property='options'),
		[Input(component_id='sectors', component_property='value'),
		Input(component_id='industries', component_property='value'),])
	def show_matching_companies(sectors, industries):
		if (not sectors or sectors is None) and (not industries or industries is None):
			return company_options_list
		try:
			industry_companies = [i for i, j in industry_per_company.items() if j in industries]
		except TypeError:
			None
		try:
			sector_companies = [i for i, j in sector_per_company.items() if j in sectors]
		except TypeError:
			None

		if not industries or industries is None:
			sector_and_industry_companies = sector_companies
		elif not sectors or sectors is None:
			sector_and_industry_companies = industry_companies
		else:
			sector_and_industry_companies = list(set(industry_companies).intersection(sector_companies))

		new_company_list = []

		for company in sector_and_industry_companies:
			new_company_list.append({'label': str(company_list[company] + ' (' + company + ')'),
									'value': company})

		return new_company_list


	@app.callback(
		Output(component_id='company_profile_data', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="api", component_property='value')])
	def collect_company_profiles(companies, api_key):
		if not companies or companies is None:
			return None
		
		company_profiles = {}
		for company in companies:
			company_profiles[company] = fa.profile(company, api_key).to_dict()
			
		return json.dumps(company_profiles)


	@app.callback(
		Output(component_id='company_profile_container', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="company_profile_data", component_property='children')])
	def display_company_profiles(companies, company_profile_data):
		if not companies or companies is None:
			return None

		data_dump = json.loads(company_profile_data)
		profiles = []

		for company in data_dump:
			
			df = pd.DataFrame(data_dump[company]['profile'], index=[company]).T
			profiles.append(html.Br())
			profiles.append(html.H5([df.loc['companyName'][0]]))
			profiles.append(html.Div(['Sector: ' + df.loc['sector'][0]]))
			profiles.append(html.Div(['Industry: ' + df.loc['industry'][0]]))
			profiles.append(html.Br())
			profiles.append(html.Div([df.loc['description'][0]]))

		return profiles


	@app.callback(
		Output(component_id='stock_data', component_property='children'),
		[Input(component_id="companies", component_property='value')])
	def collect_stock_data(companies):
		if not companies or companies is None:
			return None

		stock_data = {}
		for company in companies:
			try:
				
				# stock_data[company] = fa.stock_data(company, period="10y")['adjclose'].to_dict()
				stock_data[company] = yf.download(tickers=company, period='10y')['Close'].to_dict()
				stock_data[company] = {k.isoformat(): v for k, v in stock_data[company].items()}
				
			except Exception:
				stock_data[company] = {}

		return json.dumps(stock_data)


	@app.callback(
		Output(component_id='stock_data_container', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="data_type", component_property='value'),
		Input(component_id="stock_data", component_property='children')])
	def display_stock_data_graph(companies, data_type, stock_data):
		if not companies or companies is None:
			return None

		data_dump = json.loads(stock_data)
		traces = []

		for company in data_dump:
			df = pd.DataFrame(data_dump[company], index=[company]).T
			scatter = {'x': df.index, 'y': df[company], 'name': company}
			traces.append(scatter)

		graph = dcc.Graph(
			id='stock_data_graph',
			figure={'data': traces,
					'layout': {
						'title': 'Stock Price',
						'xaxis': {
							'nticks ': 10},
						'yaxis': {
							'type': data_type},
						"font": {
							"color": "white"
						},
						'paper_bgcolor': '#192734',
						'plot_bgcolor': '#192734',
					}
					},

			config={'displayModeBar': False},)
		


		return html.Div(graph)


	@app.callback(
		Output(component_id='key_metrics_data', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="period", component_property='value'),
		Input(component_id='key_metrics', component_property='value'),
		Input(component_id='api', component_property='value')])
	def collect_key_metrics_data(companies, period, key_metrics, api_key):
		if (not companies or companies is None) or key_metrics is None:
			return None

		key_metrics_data = {}
		for company in companies:
			key_metrics_data[company] = fa.key_metrics(company, api_key, period=period).to_dict()

		return json.dumps(key_metrics_data)


	@app.callback(
		Output(component_id='key_metrics_container', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="data_type", component_property='value'),
		Input(component_id="key_metrics_data", component_property='children'),
		Input(component_id="key_metrics", component_property="value"),
		Input(component_id='key_metrics', component_property='options')])
	def display_key_metrics_graph(companies, data_type, key_metrics_data,
								key_metrics_values, key_metrics_options):
		if (not companies or companies is None) or key_metrics_values is None:
			return None

		graphs = []
		data_dump = json.loads(key_metrics_data)
		for key in key_metrics_values:
			title = next(item for item in key_metrics_options if item["value"] == key)['label']
			traces = []
			for company in data_dump:
				df = pd.DataFrame(data_dump[company])
				data = df.loc[key]
				scatter = {'x': data.index, 'y': data.values,
						'name': company, 'type': 'bar'}
				traces.append(scatter)

			graph = dcc.Graph(
				id='graph-{}'.format(key),
				figure={'data': traces,
						'layout': {
							'height': 300,
							'xaxis': {
								'type': 'category',
								'categoryorder': 'category ascending'},
							'yaxis': {
								'type': data_type},
							"font": {
								"color": "white"
							},
							'paper_bgcolor': '#192734',
							'plot_bgcolor': '#192734',
							'title': title}},
				config={'displayModeBar': False}, style=GRAPH_STYLE)
			

			graphs.append(graph)

		return html.Div(graphs)


	@app.callback(
		Output(component_id='ratios_data', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id='financial_ratios', component_property='value'),
		Input(component_id='api', component_property='value')])
	def collect_ratios_data(companies, financial_ratios, api_key):
		if (not companies or companies is None) or financial_ratios is None:
			return None

		ratios_data = {}
		for company in companies:
			ratios_data[company] = fa.financial_ratios(company, api_key).to_dict()

		return json.dumps(ratios_data)


	@app.callback(
		Output(component_id='ratios_container', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="data_type", component_property='value'),
		Input(component_id="ratios_data", component_property='children'),
		Input(component_id="financial_ratios", component_property="value"),
		Input(component_id="financial_ratios", component_property="options")])
	def display_ratios_graphs(companies, data_type, ratios_data,
							financial_ratios_values, financial_ratios_options):
		if (not companies or companies is None) or financial_ratios_values is None:
			return None

		graphs = []
		data_dump = json.loads(ratios_data)
		for ratio in financial_ratios_values:
			title = next(item for item in financial_ratios_options if item["value"] == ratio)['label']
			traces = []
			for company in data_dump:
				df = pd.DataFrame(data_dump[company])
				data = df.loc[ratio]
				scatter = {'x': data.index, 'y': data.values,
						'name': company, 'type': 'bar'}
				traces.append(scatter)

			graph = dcc.Graph(
				id='graph-{}'.format(ratio),
				figure={'data': traces,
						'layout': {
							'height': 300,
							'xaxis': {
								'type': 'category',
								'categoryorder': 'category ascending'},
							'yaxis': {
								'type': data_type},
							"font": {
								"color": "white"
							},
							'paper_bgcolor': '#192734',
							'plot_bgcolor': '#192734',
							'title': title}},
				config={'displayModeBar': False}, style=GRAPH_STYLE)

			graphs.append(graph)

		return html.Div(graphs)


	@app.callback(
		Output(component_id='balance_sheet_data', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="period", component_property='value'),
		Input(component_id='balance_sheet_statement', component_property='value'),
		Input(component_id='api', component_property='value')])
	def collect_balance_sheet_statement_data(companies, period, balance_sheet_statement, api_key):
		if (not companies or companies is None) or balance_sheet_statement is None:
			return None

		balance_sheet_statement_data = {}
		for company in companies:
			balance_sheet_statement_data[company] = fa.balance_sheet_statement(company, api_key, period=period).to_dict()

		return json.dumps(balance_sheet_statement_data)


	@app.callback(
		Output(component_id='balance_sheet_container', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="data_type", component_property='value'),
		Input(component_id="balance_sheet_data", component_property='children'),
		Input(component_id="balance_sheet_statement", component_property="value")])
	def display_balance_sheet_statement_graphs(companies, data_type, balance_sheet_data,
											balance_sheet_statement):
		if (not companies or companies is None) or balance_sheet_statement is None:
			return None

		graphs = []
		data_dump = json.loads(balance_sheet_data)
		for item in balance_sheet_statement:
			traces = []
			for company in data_dump:
				df = pd.DataFrame(data_dump[company])
				data = df.loc[item]
				scatter = {'x': data.index, 'y': data.values,
						'name': company, 'type': 'bar'}
				traces.append(scatter)

			graph = dcc.Graph(
				id='graph-{}'.format(item),
				figure={'data': traces,
						'layout': {
							'height': 300,
							'xaxis': {
								'type': 'category',
								'categoryorder': 'category ascending'},
							'yaxis': {
								'type': data_type},
							"font": {
								"color": "white"
							},
							'paper_bgcolor': '#192734',
							'plot_bgcolor': '#192734',
							'title': item}},
				config={'displayModeBar': False}, style=GRAPH_STYLE)

			graphs.append(graph)

		return html.Div(graphs)


	@app.callback(
		Output(component_id='income_statement_data', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="period", component_property='value'),
		Input(component_id='income_statement', component_property='value'),
		Input(component_id='api', component_property='value')])
	def collect_income_statement_data(companies, period, income_statement, api_key):
		if (not companies or companies is None) or income_statement is None:
			return None

		income_statement_data = {}
		for company in companies:
			income_statement_data[company] = fa.income_statement(company, api_key, period=period).to_dict()

		return json.dumps(income_statement_data)


	@app.callback(
		Output(component_id='income_statement_container', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="data_type", component_property='value'),
		Input(component_id="income_statement_data", component_property='children'),
		Input(component_id="income_statement", component_property="value")])
	def display_income_statement_graphs(companies, data_type, income_statement_data,
										income_statement):
		if (not companies or companies is None) or income_statement is None:
			return None

		graphs = []
		data_dump = json.loads(income_statement_data)
		for item in income_statement:
			traces = []
			for company in data_dump:
				df = pd.DataFrame(data_dump[company])
				data = df.loc[item]
				scatter = {'x': data.index, 'y': data.values,
						'name': company, 'type': 'bar'}
				traces.append(scatter)

			graph = dcc.Graph(
				id='graph-{}'.format(item),
				figure={'data': traces,
						'layout': {
							'height': 300,
							'xaxis': {
								'type': 'category',
								'categoryorder': 'category ascending'},
							'yaxis': {
								'type': data_type},
							"font": {
								"color": "white"
							},
							'paper_bgcolor': '#192734',
							'plot_bgcolor': '#192734',
							'title': item}},
				config={'displayModeBar': False}, style=GRAPH_STYLE)

			graphs.append(graph)

		return html.Div(graphs)


	@app.callback(
		Output(component_id='cash_flow_statement_data', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="period", component_property='value'),
		Input(component_id='cash_flow_statement', component_property='value'),
		Input(component_id='api', component_property='value')])
	def collect_cash_flow_statement_data(companies, period, cash_flow_statement, api_key):
		if (not companies or companies is None) or cash_flow_statement is None:
			return None

		cash_flow_statement_data = {}
		for company in companies:
			cash_flow_statement_data[company] = fa.cash_flow_statement(company, api_key, period=period).to_dict()

		return json.dumps(cash_flow_statement_data)


	@app.callback(
		Output(component_id='cash_flow_statement_container', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="data_type", component_property='value'),
		Input(component_id="cash_flow_statement_data", component_property='children'),
		Input(component_id="cash_flow_statement", component_property="value")])
	def display_cash_flow_statement_graphs(companies, data_type, cash_flow_statement_data,
										cash_flow_statement):
		if (not companies or companies is None) or cash_flow_statement is None:
			return None
		graphs = []
		data_dump = json.loads(cash_flow_statement_data)
		for item in cash_flow_statement:
			traces = []
			for company in data_dump:
				df = pd.DataFrame(data_dump[company])
				data = df.loc[item]
				scatter = {'x': data.index, 'y': data.values,
						'name': company, 'type': 'bar'}
				traces.append(scatter)

			graph = dcc.Graph(
				id='graph-{}'.format(item),
				figure={'data': traces,
						'layout': {
							'height': 300,
							'xaxis': {
								'type': 'category',
								'categoryorder': 'category ascending'},
							'yaxis': {
								'type': data_type},
							"font": {
								"color": "white"
							},
							'paper_bgcolor': '#192734',
							'plot_bgcolor': '#192734',
							'title': item}},
				config={'displayModeBar': False}, style=GRAPH_STYLE)

			graphs.append(graph)

		return html.Div(graphs)


	@app.callback(
		Output(component_id='financial_statement_growth_data', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="period", component_property='value'),
		Input(component_id='financial_statement_growth', component_property='value'),
		Input(component_id='api', component_property='value')])
	def collect_financial_statement_growth_data(companies, period, financial_statement_growth, api_key):
		if (not companies or companies is None) or financial_statement_growth is None:
			return None

		financial_statement_growth_data = {}
		for company in companies:
			financial_statement_growth_data[company] = fa.financial_statement_growth(company, api_key,
																					period=period).to_dict()

		return json.dumps(financial_statement_growth_data)


	@app.callback(
		Output(component_id='financial_statement_growth_container', component_property='children'),
		[Input(component_id="companies", component_property='value'),
		Input(component_id="data_type", component_property='value'),
		Input(component_id="financial_statement_growth_data", component_property='children'),
		Input(component_id="financial_statement_growth", component_property="value")])
	def display_financial_statement_growth_graphs(companies, data_type, financial_statement_growth_data,
												financial_statement_growth):
		if (not companies or companies is None) or financial_statement_growth is None:
			return None

		graphs = []
		data_dump = json.loads(financial_statement_growth_data)
		for item in financial_statement_growth:
			traces = []
			for company in data_dump:
				df = pd.DataFrame(data_dump[company])
				data = df.loc[item]
				scatter = {'x': data.index, 'y': data.values,
						'name': company, 'type': 'bar'}
				traces.append(scatter)

			graph = dcc.Graph(
				id='graph-{}'.format(item),
				figure={'data': traces,
						'layout': {
							'height': 300,
							'xaxis': {
								'type': 'category',
								'categoryorder': 'category ascending'},
							'yaxis': {
								'type': data_type},
							"font": {
								"color": "white"
							},
							'paper_bgcolor': '#192734',
							'plot_bgcolor': '#192734',
							'title': item}},
				config={'displayModeBar': False}, style=GRAPH_STYLE)

			graphs.append(graph)

		return html.Div(graphs)

