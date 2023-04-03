#Money Mind
# stuarth-afk
# Oanda trading program
#print("hello world")
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
from oandapyV20.endpoints import orders
import pandas as pd
import math

# Oanda API access token and account ID
access_token = "dae33bc19c79e146091e2e0030757964-0464b9a0b9f2944493bf47a8645c14c0"
account_id = "101-011-25242779-001"
api = API(access_token=access_token)

# Top 10 currency pairs
currency_pairs = [
    "EUR_USD",
    "USD_JPY",
    "GBP_USD",
    "USD_CHF",
    "AUD_USD",
    "USD_CAD",
    "NZD_USD",
    "EUR_GBP",
    "EUR_JPY",
    "GBP_JPY",
]

# Define the strategy classes
class TrendingStrategy:
    def decide(self, data):
        # Code for identifying the trend and making a decision
        print("TrendingStrategy.decide executed")
        return "BUY"

class RangingStrategy:
    def decide(self, data):
        # Code for identifying support and resistance levels and making a decision
        print("RangingStrategy.decide executed")
        return "SELL"

class VolatileStrategy:
    def decide(self, data):
        # Code for managing risk in volatile markets and making a decision
        print("VolatileStrategy.decide executed")
        return "BUY"

class LowVolatilityStrategy:
    def decide(self, data):
        # Code for identifying the trend and making a decision
        print("LowVolatilityStrategy.decide executed")
        return "BUY"

class HighLiquidityStrategy:
    def decide(self, data):
        # Code for identifying support and resistance levels and making a decision
        print("HighLiquidityStrategy.decide executed")
        return "SELL"

class LowLiquidityStrategy:
    def decide(self, data):
        # Code for managing risk in volatile markets and making a decision
        print("LowLiquidityStrategy.decide executed")
        return "BUY"
class FundamentalStrategy:
    def decide(self, data):
        # Code for identifying the trend and making a decision
        print("FundamentalStrategy.decide executed")
        return "BUY"

class TechnicalStrategy:
    def decide(self, data):
        # Code for identifying support and resistance levels and making a decision
        print("TechnicalStrategy.decide executed")
        return "SELL"

class SentimentStrategy:
    def decide(self, data):
        # Code for managing risk in volatile markets and making a decision
        print("SentimentStrategy.decide executed")
        return "BUY"

class RegulatoryStrategy:
    def decide(self, data):
        # Code for identifying the trend and making a decision
        print("RegulatoryStrategy.decide executed")
        return "BUY"

class RangingStrategy:
    def decide(self, data):
        # Code for identifying support and resistance levels and making a decision
        print("RangingStrategy.decide executed")
        return "SELL"

class VolatileStrategy:
    def decide(self, data):
        # Code for managing risk in volatile markets and making a decision
        print("VolatileStrategy.decide executed")
        return "BUY"

# Function to fetch historical data
def get_historical_data(pair, granularity="D", count=100):
    params = {"granularity": granularity, "count": count}
    request = instruments.InstrumentsCandles(instrument=pair, params=params)
    api.request(request)
    print (request.response)
    return request.response

# Function to analyze market conditions and select the best trading strategy
def select_strategy(pair_data):
    # Analyze the data and choose the best strategy from the 10 strategies
    # This will require implementing the analysis logic based on the strategies mentioned above
    print("select_strategy executed")
    return "trending"

# Add new functions to get account value and execute trades
def get_account_value():
    request = accounts.AccountDetails(account_id)
    api.request(request)
    response = request.response
    account_value = float(response['account']['NAV'])
    return account_value

#function to execute a trade
def execute_trade(pair, decision):
    #Calculate the trade size based on 0.5% of the total account value * margin 50:1
    account_value = get_account_value()
    trade_value = account_value * 0.005 * 50
    
    #fetch the current price of the currency pair
    ticker = get_historical_data(pair, granularity="S5", count=1)['candles'][0]['mid']['c']
    print(f"Current price of {pair}: {ticker}")

    trade_quantity = math.floor(trade_value / float(ticker))
    
    if trade_quantity > 0:
        order_data = {
            "order": {
                "units": f"{trade_quantity}" if decision == "BUY" else f"-{trade_quantity}",
                "instrument": pair,
                "timeInForce": "FOK",
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }

        request = orders.OrderCreate(account_id, data=order_data)
        api.request(request)
        response = request.response
        print(f"{decision} order placed for {pair} with {trade_quantity} units at {ticker} price")
    else:
        print(f"Insufficient account value to place {decision} order for {pair}")



# Main function
def main():
    for pair in currency_pairs:
        pair_data = get_historical_data(pair)
        strategy = select_strategy(pair_data)
        print(f"Selected strategy for {pair}: {strategy}")

        # Initialize strategy objects
        trending_strategy = TrendingStrategy()
        ranging_strategy = RangingStrategy()
        volatile_strategy = VolatileStrategy()
        low_volatility_strategy = LowVolatilityStrategy()
        high_liquidity_strategy = HighLiquidityStrategy()
        low_liquidity_strategy = LowLiquidityStrategy()
        fundamental_strategy = FundamentalStrategy()
        technical_strategy = TechnicalStrategy()
        sentiment_strategy = SentimentStrategy()
        regulatory_strategy = RegulatoryStrategy()

        #initialise decision variable
        decision = None

        # Execute the selected strategy
        if strategy == "trending":
            decision = trending_strategy.decide(pair_data)
        elif strategy == "ranging":
            decision = ranging_strategy.decide(pair_data)
        elif strategy == "volatile":
            decision = volatile_strategy.decide(pair_data)
        elif strategy == "low_volatility":
            decision = low_volatility_strategy.decide(pair_data)
        elif strategy == "high_liquidity":
            decision = high_liquidity_strategy.decide(pair_data)
        elif strategy == "low_liquidity":
            decision = low_liquidity_strategy.decide(pair_data)
        elif strategy == "fundamental":
            decision = fundamental_strategy.decide(pair_data)
        elif strategy == "technical":
            decision = technical_strategy.decide(pair_data)
        elif strategy == "sentiment":
            decision = sentiment_strategy.decide(pair_data)
        elif strategy == "regulatory":
            decision = regulatory_strategy.decide(pair_data)

        # Call get_account_value() and execute_trade() if the decision is "BUY" or "SELL"
        if decision in ["BUY","SELL"]:
            print("Account Value:", get_account_value())
            execute_trade(pair, decision)




if __name__ == "__main__":
    main()


