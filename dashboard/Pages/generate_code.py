import os

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import yfinance as yf
import pandas as pd

PRIMARY = '#FFFFFF'
SECONDARY = '#FFFFFF'
ACCENT = '#98C1D9'
SIDEBAR = '#F7F7F7'
DARK_ACCENT = '#474747'

def make_layout():

	left_col = html.Div([
		dbc.Card(
			dbc.CardBody([
				html.Br(),
				dbc.Row([
					dbc.Col([
						dbc.Card(
							[dbc.CardHeader('Choose ticker/tickers', style={'color': DARK_ACCENT}),
							dbc.CardBody([
								html.Div([
									dcc.Dropdown(
										id='symbols',
										options=[{'label': name, 'value': name} for name in pd.read_csv('dashboard/Static/sp500_companies.csv')['Symbol'].to_list()],
										#options=['AAPL', 'TSLA', 'MSFT', 'AMZN'], #Replace this with list
										multi=True)
								]),
							])], color=PRIMARY, style={'border-radius': 10}
						),
						html.Br(),
						dbc.Card(
							[
								dbc.CardHeader('Generate Algorithm Code', style={'color': DARK_ACCENT}),
								dbc.CardBody([
								# Generate code
								html.Div([
									html.Div('Sample Strategies:', className='four columns'),
									dcc.Dropdown(id='module-gc', options=[], className='eight columns u-pull-right')
									# dcc.Dropdown(
									#     id='module',
									#     options=[{'label': name, 'value': name} for name in oc.cfg['backtest']['modules'].split(',')],
									#     className='eight columns u-pull-right')
								], className='row mb-10'),
								html.Br(),
								html.Div([
									html.Div('Strategy Name:', className='four columns'),
									#dcc.Dropdown(id='strategy', options=[], className='eight columns u-pull-right')
									dcc.Input(id='filename', className='eight columns u-pull-right', value = "MyStrategy", style={'margin-left': '10px', 'width': '150px', 'font-size': '15px', 'font-weight': '5', 'border-radius': 5})
								], className='row mb-8'),

								html.Br(),

								html.Div([
									html.Div('Capital:', className='four columns'),
									#dcc.Dropdown(id='strategy', options=[], className='eight columns u-pull-right')
									dcc.Input(id='cash', className='eight columns u-pull-right', value = 10000, style={'margin-left': '10px', 'width': '150px', 'font-size': '15px', 'font-weight': '5', 'border-radius': 5})
								], className='row mb-10'),
								html.Br(),

								html.Button('Generate Code', id='save-btn', n_clicks=0, className='eight columns u-pull-right', style={'font-size': '15px', 'font-weight': '5', 'color': PRIMARY, 'background-color': ACCENT, "border-color":ACCENT, 'border-radius': 5}),
							]),], color=PRIMARY, style={'border-radius': 10}
						),
						html.Div(id='code-generated-gc', style={'display': 'none'}),
						html.Div(id='code-generated2-gc', style={'display': 'none'}),
					], width=4)
				], id='graph-container', style={'margin-bottom':'30rem'})
			]),
		),
	])

	return left_col


def register_callbacks(app):
	# @app.server.route('{}<file>'.format(static_route))
	# def serve_file(file):
	# 	if file not in stylesheets and file not in jss:
	# 		raise Exception('"{}" is excluded from the allowed static css files'.format(file))
	# 	static_directory = os.path.join(root_directory, 'Static')
	# 	return flask.send_from_directory(static_directory, file)

	@app.callback(Output('module-gc', 'options'), [Input('symbols', 'value')])
	def update_algo_list(symbols):

		all_files = os.listdir("dashboard/SampleStrategies") 
		algo_files = list(filter(lambda f: f.endswith('.py'), all_files))
		algo_avlb = [s.rsplit( ".", 1 )[ 0 ] for s in algo_files]
		#print(algo_avlb)    
		return algo_avlb

	# @app.callback(Output('strategy', 'options'), [Input('module', 'value')])
	# def update_strategy_list(module_name):
	#     data = ob.test_list(module_name)
	#     return [{'label': name, 'value': name} for name in data]

	@app.callback(Output('strategy-gc', 'options'), [Input('symbols', 'value')])
	def update_strategy_list(symbols):  
		print("strat called")
		all_files = os.listdir("MyStrategies")    
		backtest_files = list(filter(lambda f: f.endswith('.py'), all_files))
		backtest_avlb = [s.rsplit( ".", 1 )[ 0 ] for s in backtest_files]  
		#print(backtest_avlb) 
		return backtest_avlb

	# I think this callback is not needed. No html tag with id = 'params-table' is there
	# Commenting out it for now.

	# @app.callback(Output('params-table', 'columns'), [Input('module', 'value'), Input('strategy', 'value'), Input('symbols', 'value')])
	# def update_params_list(module_name, strategy_name, symbol):
	#     return ob.params_list(module_name, strategy_name, symbol)


	@app.callback(Output('strategy-gc', 'value'), [Input('strategy-gc', 'options')])
	def update_strategy_value(options):
		if len(options):
			#print(options)
			return options[0]
		return ''

	#Add code later to make sure that enter cash and symbols
	@app.callback(Output('code-generated-gc', 'children'),
				[
					Input('save-btn', 'n_clicks'),
					Input('cash', 'value'),
					Input('module-gc', 'value'),
					Input('symbols', 'value'),
					Input('filename', 'value'),
				])
	def create_code(n_clicks, cash, module, symbols, filename):
		if n_clicks == 0:
			return '' 

		data = data2 = ""
		
		backtest_code = '''                

	def backtest():
		cash = {cash}
		symbols = {symbols}
		#start_date = '2018-01-01'
		data_dir = "Data/"  

		cerebro = bt.Cerebro()
		cerebro.broker.setcash(cash)

		for s in symbols:            
				df = pd.read_csv(os.path.join(data_dir, s+".csv"), parse_dates=True, index_col=0)
				data = bt.feeds.PandasData(dataname=df)
				cerebro.adddata(data)
		# Strategy
		cerebro.addstrategy({module})


		cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
		cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
		cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')
		cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
		
		# Backtest 
		
		print('Starting Portfolio Value: ',  cerebro.broker.getvalue())
		plt.rcParams['figure.figsize']=[10,6]
		plt.rcParams["font.size"]="12"

		# Run over everything
		results = cerebro.run()
		pnl = cerebro.broker.getvalue() - cash
		#cerebro.plot()
		# Print out the final result
		print('Final Portfolio Value: ',  cerebro.broker.getvalue()) 
		
		return pnl, results[0]    

	#end of function for '{symbols}' with capital '{cash}'
			
					'''.format(symbols=symbols, cash = cash, module = module)

		strategy_file=module+".py"
		strategy_file = "dashboard/SampleStrategies/"+strategy_file

		with open(strategy_file) as fp:
			data = fp.read()
		
		
		data += "\n"
		data += backtest_code
		path_dir = "dashboard/MyStrategies/"
		filename_save = filename+".py"
		
		with open (os.path.join(path_dir, filename_save), 'w') as fp:
			fp.write(data)
			
		return 0

		#####  Download Button #####

	# @app.callback(Output('code-generated2-gc', 'children'),
	# 			[
	# 				Input('download-btn', 'n_clicks'),
	# 				Input('symbols', 'value')
	# 			])
	# def download_data(n_clicks, symbols ):
	# 	if n_clicks == 0:
	# 		return '' 
	# 	#symbols = ['TSLA', 'GE']
	# 	print("testing Datas ") 
	# 	print(symbols)   
	# 	for s in symbols:
	# 			df = yf.download(s, start = "2018-01-01")
	# 			data_dir = "Data/"
	# 			filename = s +".csv"
	# 			df.to_csv(os.path.join(data_dir, filename)) 
	# 	#return dcc.send_data_frame(df.to_csv, filename) 
	# 	# module_name = "FromBackTrader"
	# 	# module = importlib.import_module(module_name)
	# 	# pnl, results = module.backtest()
	# 	#result = subprocess.getstatusoutput('python FromBackTrader.py' )  
	# 	return 0