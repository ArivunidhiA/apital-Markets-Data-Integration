import os
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime, timedelta
import dash
from dash import html, dcc, Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Function to fetch market data using yfinance
def fetch_market_data(symbols, period='1mo'):
    data = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            data[symbol] = hist
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return data

# Function to fetch SEC filings using EDGAR API
def fetch_sec_filings(company_cik, filing_type='10-K'):
    headers = {'User-Agent': 'Mozilla/5.0'}
    base_url = f"https://data.sec.gov/submissions/CIK{company_cik.zfill(10)}.json"
    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            recent_filings = data.get('filings', {}).get('recent', {})
            if recent_filings:
                forms = recent_filings.get('form', [])
                dates = recent_filings.get('filingDate', [])
                return pd.DataFrame({'form': forms, 'date': dates})
    except Exception as e:
        print(f"Error fetching SEC filings: {e}")
    return pd.DataFrame()

# Initial data load
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
market_data = fetch_market_data(symbols)

# Dashboard layout
app.layout = html.Div([
    html.H1("Capital Markets Data Integration Dashboard",
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    # Market Overview Section
    html.Div([
        html.H2("Market Overview", style={'color': '#34495e'}),
        dcc.Dropdown(
            id='stock-selector',
            options=[{'label': symbol, 'value': symbol} for symbol in symbols],
            value='AAPL',
            style={'width': '50%', 'marginBottom': '20px'}
        ),
        dcc.Graph(id='stock-price-chart'),
        
        # Performance Metrics
        html.Div([
            html.Div(id='performance-metrics', className='metrics-container')
        ], style={'marginTop': '20px'})
    ], style={'padding': '20px', 'backgroundColor': '#f7f9fc', 'borderRadius': '10px', 'marginBottom': '20px'}),
    
    # Regulatory Filings Section
    html.Div([
        html.H2("Recent SEC Filings", style={'color': '#34495e'}),
        html.Div(id='sec-filings-table')
    ], style={'padding': '20px', 'backgroundColor': '#f7f9fc', 'borderRadius': '10px'}),
    
    # Update Interval
    dcc.Interval(
        id='interval-component',
        interval=300*1000,  # updates every 5 minutes
        n_intervals=0
    )
])

# Callback for updating stock price chart
@app.callback(
    Output('stock-price-chart', 'figure'),
    [Input('stock-selector', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_stock_chart(selected_stock, n):
    if not selected_stock:
        raise PreventUpdate
    
    df = market_data[selected_stock]
    
    figure = {
        'data': [
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=selected_stock
            )
        ],
        'layout': {
            'title': f'{selected_stock} Stock Price',
            'yaxis': {'title': 'Price (USD)'},
            'xaxis': {'title': 'Date'},
            'template': 'plotly_white'
        }
    }
    return figure

# Callback for updating performance metrics
@app.callback(
    Output('performance-metrics', 'children'),
    [Input('stock-selector', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_metrics(selected_stock, n):
    if not selected_stock:
        raise PreventUpdate
    
    df = market_data[selected_stock]
    current_price = df['Close'][-1]
    daily_return = ((df['Close'][-1] - df['Close'][-2]) / df['Close'][-2]) * 100
    volatility = df['Close'].pct_change().std() * np.sqrt(252) * 100
    
    metrics = [
        html.Div([
            html.H4('Current Price'),
            html.P(f'${current_price:.2f}')
        ], className='metric-box'),
        html.Div([
            html.H4('Daily Return'),
            html.P(f'{daily_return:.2f}%')
        ], className='metric-box'),
        html.Div([
            html.H4('Annualized Volatility'),
            html.P(f'{volatility:.2f}%')
        ], className='metric-box')
    ]
    
    return metrics

# Callback for updating SEC filings
@app.callback(
    Output('sec-filings-table', 'children'),
    [Input('stock-selector', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_sec_filings(selected_stock, n):
    # CIK mapping (you would need to maintain this mapping or fetch it dynamically)
    cik_mapping = {
        'AAPL': '0000320193',
        'MSFT': '0000789019',
        'GOOGL': '0001652044',
        'AMZN': '0001018724',
        'META': '0001326801'
    }
    
    if selected_stock not in cik_mapping:
        return html.P("No SEC filing data available")
    
    filings_df = fetch_sec_filings(cik_mapping[selected_stock])
    if filings_df.empty:
        return html.P("No recent SEC filings found")
    
    # Create table
    table = html.Table([
        html.Thead(
            html.Tr([html.Th("Filing Type"), html.Th("Date")])
        ),
        html.Tbody([
            html.Tr([
                html.Td(filing['form']),
                html.Td(filing['date'])
            ]) for _, filing in filings_df.head(5).iterrows()
        ])
    ], style={'width': '100%', 'textAlign': 'left'})
    
    return table

if __name__ == '__main__':
    app.run_server(debug=True)
