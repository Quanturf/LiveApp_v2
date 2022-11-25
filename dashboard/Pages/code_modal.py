

def get_modal_content(pathname, symbol):
    if not symbol or symbol is None:
            symbol = 'desired symbol'
        
    code_dict = {}
    
    equity_code = '''
                **Packages**
                ```python 
                import numpy as np
                import pandas as pd

                # Market Data 
                from pandas_datareader import data as pdr
                import yfinance as yf
                import yahoo_fin.stock_info as si
                ```
                **Moving Averages**
                ```python
                # Override Yahoo Finance 
                yf.pdr_override()

                # Create input field for our desired stock 
                stock = '{symbol}'

                # Retrieve stock data frame (df) from yfinance API at an interval of 1m 
                df = yf.download(tickers=stock,period='1d',interval='1m')

                # add Moving Averages (5day and 20day) to df 
                df['MA5'] = df['Close'].rolling(window=5).mean()
                df['MA20'] = df['Close'].rolling(window=20).mean()
                ```
                ### Various Data frames

                **EPS Trend**
                ```python

                ticker = '{symbol}'
                df = si.get_analysts_info(ticker)['EPS Trend'].assign(hack='').set_index('hack')
                ```
                **Growth Estimates** 
                ```python
                ticker = '{symbol}'
                df = si.get_analysts_info(ticker)['Growth Estimates'].assign(hack='').set_index('hack')

                ```
                **Earnings Estimates** 
                ```python
                ticker = '{symbol}'
                df = si.get_analysts_info(ticker)['Earnings Estimate'].assign(hack='').set_index('hack')
                ```
                **Revenue Estimate** 
                ```python
                ticker = '{symbol}'
                df = si.get_analysts_info(ticker)['Revenue Estimate'].assign(hack='').set_index('hack')
                ```
                **Earnings History** 
                ```python
                ticker = '{symbol}'
                df = si.get_analysts_info(ticker)['Earnings History'].assign(hack='').set_index('hack')
                ```
                **EPS Revisions** 
                ```python
                ticker = '{symbol}'
                df = si.get_analysts_info(ticker)['EPS Revisions'].assign(hack='').set_index('hack')

                ```
                **Income Statement** 
                ```python

                ticker = '{symbol}'
                data = yf.Ticker(ticker)

                df = pd.DataFrame(data.financials).T
                ```
                **Statement of Cash Flows** 
                ```python

                ticker = '{symbol}'
                data = yf.Ticker(ticker)

                df = pd.DataFrame(data.cashflow).T
                ```
                **Balance Sheet** 
                ```python

                ticker = '{symbol}'
                data = yf.Ticker(ticker)

                df = pd.DataFrame(data.balance_sheet).T

                ```
                '''.format(symbol=symbol)
    code_dict['/backtest'] = equity_code
    code_dict['/'] = equity_code
    code_dict['/home'] = equity_code

    code_dict['/equity-visuals'] = '''
                **Packages**
                ```python 
                import FundamentalAnalysis as fa
                import yfinance as yf


                api_key = [Get Key Here](https://site.financialmodelingprep.com/developer/docs/)
                period = 'annual' # quarterly also possible
                ```

                **Company Profiles**
                ```python
                data = fa.profile('{symbol}', api_key).to_dict()
                ```
                **Stock Data**
                ```python
                data = yf.download(tickers='{symbol}', period='10y')['Close'].to_dict()
                ```
                **Key Metrics**
                ```python
                data = fa.key_metrics('{symbol}', api_key, period=period).to_dict()
                ```
                **Financial Ratios**
                ```python
                data = fa.financial_ratios('{symbol}', api_key).to_dict()
                ```
                **Balance Sheet**
                ```python
                data = fa.balance_sheet_statement('{symbol}', api_key, period=period).to_dict()
                ```
                **Income Statement**
                ```python
                data = fa.income_statement('{symbol}', api_key, period=period).to_dict()
                ```
                **Statement of Cash Flows**
                ```python
                data = fa.cash_flow_statement('{symbol}', api_key, period=period).to_dict()
                ```
                **Financial Statement Growth**
                ```python
                data = fa.financial_statement_growth('{symbol}', api_key,period=period).to_dict()
                ```
                '''.format(symbol=symbol)

    code_dict['/crypto'] = '''
                **Packages**
                ```python 
                import yfinance as yf

                ```
                **Crypto Moving Average**
                ```python
                # Override Yahoo Finance 
                yf.pdr_override()

                # Create input field for our desired stock 
                crypto = '{symbol}'

                # Retrieve stock data frame (df) from yfinance API at an interval of 1m 
                df = yf.download(tickers=crypto,period='1d',interval='1m')

                # add Moving Averages (5day and 20day) to df 
                df['MA5'] = df['Close'].rolling(window=5).mean()
                df['MA20'] = df['Close'].rolling(window=20).mean()
                ```

                '''.format(symbol=symbol)
    code_dict['/FX'] = '''
                **Packages**
                ```python 
                import yfinance as yf


                # API Requests for news div
                news_requests = requests.get(
                    "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=da8e2e705b914f9f86ed2e9692e66012"
                )
                ```
                **News Data**
                ```python
                json_data = news_requests.json()["articles"]
                df = pd.DataFrame(json_data)
                df = pd.DataFrame(df[["title", "url"]])
                ```
                '''.format(symbol=symbol)
    return code_dict[pathname]