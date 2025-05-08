# API Stock Trader Bot

A simple microservice-based stock trading bot for CS361. This app allows users to register, log in, retrieve stock prices, and manage a paper trading portfolio.

## Features

- User registration and login
- Real-time stock quotes using Alpha Vantage
- Simulated stock buy/sell
- Portfolio tracking

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your_username/api-stock-trader-bot.git
cd api-stock-trader-bot
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API key:
```
AV_KEY=your_alpha_vantage_api_key
```

4. Run the app:
```bash
python main.py
```

## License

This project is licensed under the MIT License.
