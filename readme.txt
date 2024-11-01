# Capital Markets Data Integration Dashboard

## Project Overview
This dashboard provides real-time monitoring and analysis of market data and regulatory filings for major technology companies. It integrates data from Yahoo Finance and SEC EDGAR APIs to provide a comprehensive view of market movements and regulatory compliance information.

## Features
- Real-time stock price monitoring with candlestick charts
- Key performance metrics including current price, daily returns, and volatility
- SEC filings tracker for regulatory compliance
- Automatic data updates every 5 minutes
- Interactive stock selection and visualization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/capital-markets-dashboard.git
cd capital-markets-dashboard
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:8050`

## Data Sources
- Market Data: Yahoo Finance API (via yfinance)
- Regulatory Filings: SEC EDGAR API

## User Stories

### For Portfolio Managers
- As a portfolio manager, I want to monitor real-time price movements of key tech stocks
- As a portfolio manager, I want to analyze stock volatility and performance metrics
- As a portfolio manager, I want to be alerted to significant price movements

### For Compliance Officers
- As a compliance officer, I want to track recent SEC filings for regulatory monitoring
- As a compliance officer, I want to receive notifications of new regulatory filings
- As a compliance officer, I want to access historical filing data for audit purposes

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
