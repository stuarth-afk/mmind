#Money Mind
# stuarth-afk
# Oanda trading program

import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
from oandapyV20.endpoints import orders
import pandas as pd
import math
import threading
import time
import datetime
import pytz
import numpy as np
import configparser

# Oanda API access token and account ID
access_token = "dae33bc19c79e146091e2e0030757964-0464b9a0b9f2944493bf47a8645c14c0"
account_id = "101-011-25242779-001"
api = API(access_token=access_token)

# Top 10 currency pairs
currency_pairs = [
    "EUR_USD",
    "AUD_USD",
    #"USD_JPY", #Do not enable Japanese Currency Pair, it needs logic to allow for greater pip size
    "GBP_USD",
    "USD_CHF",
    "USD_CAD",
    "NZD_USD",
    "EUR_GBP",
    #"EUR_JPY", #Do not enable Japanese Currency Pair, it needs logic to allow for greater pip size
    #"GBP_JPY", #Do not enable Japanese Currency Pair, it needs logic to allow for greater pip size
]

# Create global flag variables for each currency pair
for currency in currency_pairs:
    globals()[currency + "_flag"] = False
    globals()[currency + "_flag_expiry_time"] = 0

# Global moving average variables
current_price = 0
ma5 =  0
ma10 = 0
ma20 = 0
ma50 = 0
ma100 = 0

#Global Program Settings
NUM_POINTS = 101

# Define the strategy classes
class TrendingStrategy:
    #def __init__(self, pair):
    #    self.pair = pair
        
    def decide(self, data):
        global ma5, ma20, ma50
        
        # Get the current market price for the currency pair
        #market_price = data['price'].iloc[-1]
        market_price = float(data['candles'][-1]['mid']['c'])
        #Print the current market price
        #print(f"Market Price:", market_price)

        #DEBUG FORCE CODE
        #return "SELL"

        # Determine whether the market is trending up or down based on the moving averages
        if ma5 > ma20 > ma50 and market_price > ma5:
            # The market is trending up and the current price is above the 5-candle moving average, so execute a "BUY"
            print("BUY")
            return "BUY"
        elif ma5 < ma20 < ma50 and market_price < ma5:
            # The market is trending down and the current price is below the 5-candle moving average, so execute a "SELL"
            print("SELL")
            return "SELL"
        else:
            # The market is not trending or the current price is between the moving averages, so do not execute a trade
            print("NO ACTION")
            return "NO ACTION"

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
        # Code for identifying a Regulatory market and making a decision
        print("RegulatoryStrategy.decide executed")
        return "BUY"

# Function to fetch historical data
def get_historical_data(pair, granularity="M1", count=NUM_POINTS):
    try:
        params = {"granularity": granularity, "count": count}
        request = instruments.InstrumentsCandles(instrument=pair, params=params)
        api.request(request)
        #print (request.response)
        return request.response
    except Exception as e:
        print(f"Fetch Error Occurred in get_historical_data: {e}")
    return

# Function to process data and calculate moving averages
def process_data_and_calculate_moving_averages(candles):
    # Process the data and create a pandas DataFrame
    data = pd.DataFrame([{
        'time': candle['time'],
        'Close': float(candle['mid']['c'])
    } for candle in candles])

    # Calculate moving averages
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA10'] = data['Close'].rolling(window=10).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA100'] = data['Close'].rolling(window=100).mean()

    # Assign the most recent moving average values to global variables
    global current_price 
    global ma5 
    global ma10 
    global ma20
    global ma50 
    global ma100

    current_price = round(float(data['MA5'].iloc[-1]),4)
    ma5 = round(float(data['MA5'].iloc[-1]),4)
    ma10 = round(float(data['MA10'].iloc[-1]),4)
    ma20 = round(float(data['MA20'].iloc[-1]),4)
    ma50 = round(float(data['MA50'].iloc[-1]),4)
    ma100 = round(float(data['MA100'].iloc[-1]),4)

    return data

# Function to analyze market conditions and select the best trading strategy
def select_strategy(pair, pair_data):
    # Analyze the data and choose the best strategy from the 10 strategies
    # This will require implementing the analysis logic based on the strategies mentioned above

    if pair == "EUR_USD":
        #print("EUR_USD Market to apply a Trending Strategy")
        return "trending"
    elif pair == "AUD_USD":
        #print("AUD_USD Market to apply a Trending Strategy")
        return "trending"
    else :
        #print("Default Trending Strategy Selected")
        return "trending"

# Get account value and other details
def get_account_value():
    try:
        request = accounts.AccountDetails(account_id)
        api.request(request)
        response = request.response
        account_value = float(response['account']['NAV'])
        return account_value
    except:
         print("Fetch Error Occurreed in get_account_value()")
    return

# Function to execute a trade order to Oanda
def execute_trade(pair, decision):
    # Include Global Flags in this function to limit how many orders are placed for each currency pair.
    for currency in currency_pairs:
        if currency == pair:
            tagname_expiry_flag = currency + "_flag"
            tagname_expiry_time = currency + "_flag_expiry_time"
            break

    # If the expiry flag is set, then do not execute this function
    if globals()[pair + "_flag"] == True:
        print("Expiry Flag True - Order can not be placed until:",globals()[tagname_expiry_time])
        return

    #Define Stop Loss Distance
    stop_loss_distance = 0.0005 # set this to desired number of pips
    take_profit_distance = 0.00025 # set this to desired number of pips 

    #Define the opportunity to buy window
    buy_below_distance = 0.0000 #0.0010 set this to desired number of pips below current price for a BUY trade
    buy_above_distance = 0.0000 #0.0010 set this to desired number of pips above current price for a SELL trade
    
    # Calculate the trade size based on 0.5% of the total account value * margin 50:1
    account_value = get_account_value()
    trade_value = account_value * 0.005 * 50

    # fetch the current price of the currency pair
    ticker = get_historical_data(pair, granularity="S5", count=1)['candles'][0]['mid']['c']
    print(f"5S Candle Updated Price of {pair}: {ticker}")

    trade_quantity = math.floor(trade_value / float(ticker))

    #set the price that a buy/sell will occur
    if decision == "BUY":
         opportunity_price = round(float(ticker)  - buy_below_distance,5) # set to x pips below current price for a BUY
    elif decision == "SELL":
        opportunity_price = round(float(ticker)  + buy_above_distance,5) # set to x pips above current price for a SELL
    else :
        opportunity_price = 0 # set to 0 for NO ACTION

    # Set expiry time in UTC
    expiry_time_utc = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

    # Convert expiry time to AEST timezone
    tz_aest = pytz.timezone('Australia/Sydney')
    expiry_time_aest = expiry_time_utc.astimezone(tz_aest)
    #allow_next_order_time_aest = expiry_time_utc.astimezone(tz_aest)

    # Format expiry time as string in the expected format
    expiry_time_str = expiry_time_aest.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Once the trade is executed, set the corresponding flag to True
    globals()[tagname_expiry_flag] = True
    #print("Expiry Flag:", globals()[tagname_expiry_flag])

    # Once the trade is executed, set the corresponding flag_expiry_time
    globals()[tagname_expiry_time] = expiry_time_aest
    #flag_expiry_time = globals()[pair + "_flag_expiry_time"]
    #print("DEBUG 8 Flag Expiry Time:",globals()[tagname_expiry_time])

    # Define a function to set the flag back to False when the expiry time is reached
    def set_flag_false():
        globals()[tagname_expiry_flag] = False
        globals()[tagname_expiry_time]= 0

    # Schedule the set_flag_false function to be called after the expiry time has passed
    timer = threading.Timer((expiry_time_utc - datetime.datetime.utcnow()).total_seconds(), set_flag_false)
    timer.start()

    if trade_quantity > 0:
        order_data = {
            "order": {
                "units": f"{trade_quantity}" if decision == "BUY" else f"-{trade_quantity}",
                "price": str(opportunity_price),
                "instrument": pair,
                "timeInForce": "GTD",
                "type": "LIMIT",
                "gtdTime": expiry_time_str,
                "positionFill": "DEFAULT",
                #"trailingStopLossOnFill": {      #Pat uses stop loss on fill with MARKET, then updates the stop loss using the "trade" endpoint. Not the "order" endpoint. Pat trades 1 minute candles, and will bump up the stop loss to be 2 pips below the lowest candle in the last 15 minutes.
                    "distance": str(stop_loss_distance),
                #    "timeInForce": "GTC",
                #    "type": "TRAILING_STOP_LOSS"
                "takeProfitOnFill": {          # Add this block to set a take profit condition
                     "price": str(round((opportunity_price + take_profit_distance),5)) if decision == "BUY" else str(round((opportunity_price - take_profit_distance),5)),
                     "timeInForce": "GTC" 
                },
                "trailingStopLossOnFill": {
                    "distance": str(stop_loss_distance),
                    "timeInForce": "GTC",
                    "type": "TRAILING_STOP_LOSS"
                }
            }
        }

        try:
            #time.sleep(10) # Pause not required
            #print(f"DEBUG 4 {decision} order placed for {pair} with {trade_quantity} units at {opportunity_price} with stop loss {stop_loss_distance} opportunity price to expire {expiry_time_str} ")
            request = orders.OrderCreate(account_id, data=order_data)
            api.request(request)
            response = request.response
            print(f"{decision} order placed for {pair} with {trade_quantity} units at {opportunity_price} opportunity price")
        except Exception as e:
            print(f"ORDER ERROR: {decision} order placed for {pair} with {trade_quantity} units at {opportunity_price} with stop loss {stop_loss_distance} opportunity price to expire {expiry_time_str} ")           
            print(f"Request Order Error Occurred in execute_trade: {e}")
    else:
        print(f"Insufficient account value to place {decision} order for {pair}")

# Main function
def main():
    for pair in currency_pairs:
        #DEBUG 6 
        #print("EUR_USD Expiry Flag:",EUR_USD_flag)
        #print("EUR_USD Expiry Time:",EUR_USD_flag_expiry_time)
        #print("AUD_USD Expiry Flag:",AUD_USD_flag)
        #print("AUD_USD Expiry Time:",AUD_USD_flag_expiry_time)

        pair_data = get_historical_data(pair)
        
        # Process the data and calculate moving averages
        candles = pair_data['candles']
        moving_avg_data = process_data_and_calculate_moving_averages(candles)

        # Print the DataFrame with the calculated moving averages
        #print(moving_avg_data)

        strategy = select_strategy(pair, pair_data)

        # Print Values to Command Line
        print(f"\n{pair} Current Price:", current_price)
        print(f"Strategy:{strategy}")
        print("Moving Averages")
        print("MA5  :", ma5)
        print("MA10 :", ma10)
        print("MA20 :", ma20)
        print("MA50 :", ma50)
        print("MA100:", ma100)

        #strategy = select_strategy(pair, pair_data)
        #print(f"Selected strategy for {pair}: {strategy}")

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

#if __name__ == "__main__":
#    main()

while True:
    config = configparser.ConfigParser()
    config.read('config.ini')

    setting1 = config.get('general', 'setting1')
    setting2 = config.get('general', 'setting2')

    db_host = config.get('database', 'host')
    db_port = config.getint('database', 'port')
    db_user = config.get('database', 'user')
    db_password = config.get('database', 'password')

    # Now you can use the config values in your script
    print("Current Settings: ",setting1, setting2, db_host, db_port, db_user, db_password)

    main() # Call main function

    time.sleep(30) # Pause the while loop for 30 seconds
