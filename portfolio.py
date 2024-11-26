import json
import urllib.request


class StockPortfolio:
    def __init__(self, api_key):
        self.api_key = api_key
        self.portfolio = {}

    def add_stock(self, symbol, shares):
        if symbol in self.portfolio:
            self.portfolio[symbol]['shares'] += shares
        else:
            self.portfolio[symbol] = {'shares': shares, 'price': 0}
        print(f"Added {shares} shares of {symbol} to your portfolio.")

    def remove_stock(self, symbol):
        if symbol in self.portfolio:
            del self.portfolio[symbol]
            print(f"Removed {symbol} from your portfolio.")
        else:
            print(f"{symbol} not found in your portfolio.")

    def fetch_stock_price(self, symbol):
        base_url = "https://www.alphavantage.co/query"
        query_params = (
            f"?function=TIME_SERIES_INTRADAY&symbol={symbol}"
            f"&interval=1min&apikey={self.api_key}"
        )
        url = base_url + query_params

        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                latest_time = list(data["Time Series (1min)"].keys())[0]
                return float(data["Time Series (1min)"][latest_time]["4. close"])
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None

    def update_prices(self):
        for symbol in self.portfolio.keys():
            price = self.fetch_stock_price(symbol)
            if price is not None:
                self.portfolio[symbol]['price'] = price

    def display_portfolio(self):
        print("\nYour Portfolio:")
        total_value = 0
        for symbol, details in self.portfolio.items():
            value = details['shares'] * details['price']
            total_value += value
            print(f"{symbol}: {details['shares']} shares @ ${details['price']:.2f} each (Total: ${value:.2f})")
        print(f"Total Portfolio Value: ${total_value:.2f}\n")


# Replace 'your_api_key' with your Alpha Vantage API key
API_KEY = "your_api_key"
portfolio = StockPortfolio(API_KEY)

# Example Usage
portfolio.add_stock("AAPL", 10)
portfolio.add_stock("MSFT", 5)
portfolio.update_prices()
portfolio.display_portfolio()
portfolio.remove_stock("MSFT")
portfolio.update_prices()
portfolio.display_portfolio()

