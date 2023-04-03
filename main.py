#Money Mind
# stuarth-afk
# Oanda traing program
#print("hello world")
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
import pandas as pd

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
    print("select_strategy function run")
    return "best_strategy"

# Main function
def main():
    for pair in currency_pairs:
        pair_data = get_historical_data(pair)
        print("pair data for "+str(pair)+" data: "+ str(pair_data))
        strategy = select_strategy(pair_data)
        print(f"Selected strategy for {pair}: {strategy}")
        # Execute the trading strategy based on the market conditions

if __name__ == "__main__":
    main()


