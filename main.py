# Money Mind
# stuarth-afk
# Oanda Currency Trading Program

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

# Global variable to keep track of the first scan
is_first_scan = True

# Global moving average and other data variables
current_price = 0
ma5 =  0
ma10 = 0
ma20 = 0
ma50 = 0
ma100 = 0
current_rsi = 50   

#Global Program Settings
#NUM_POINTS = 101  # replaced with num_candles_to_fetch

# Define the strategy classes
class TrendingStrategy1:        
    def __init__(self, settings):
        self.upper_rsi = settings['upper_rsi']
        self.lower_rsi = settings['lower_rsi']
        
    def decide(self, data):
        global ma5, ma10, ma20, ma50, ma100, current_rsi

        # Get the current market price for the currency pair
        market_price = float(data['candles'][-1]['mid']['c'])
        #print(f"Market Price:", market_price)

        #DEBUG FORCE CODE
        #return "BUY"
        
        print("Upper RSI SETTING:", self.upper_rsi )
        print("Current RSI:", current_rsi )
        print("Lower RSI SETTING:", self.lower_rsi,"\n" )   
            
        # Determine whether the market is trending up or down based on the moving averages 
        if ma5 > ma20 > ma50 and market_price > ma5 and current_rsi > 30 and current_rsi < self.lower_rsi :
            # The market is trending up and the current price is above the 5-candle moving average and the RSI is above oversold level(30) and below individual pair lower setting, so execute a "BUY"
            print("BUY")
            return "BUY"
        elif ma5 < ma20 < ma50 and market_price < ma5 and current_rsi < 70 and current_rsi < self.upper_rsi :
            # The market is trending down and the current price is below the 5-candle moving average and the RSI is below the overbought level(70) and above individual pair upper setting, so execute a "SELL"
            print("SELL")
            return "SELL"
        else:
            # The market is not trending or the current price is between the moving averages, so do not execute a trade
            print("NO ACTION")
            return "NO ACTION"

class TrendingStrategy2:        
    def __init__(self, settings):
        self.upper_rsi = settings['upper_rsi']
        self.lower_rsi = settings['lower_rsi']
        
    def decide(self, data):
        global ma5, ma10, ma20, ma50, ma100, current_rsi

        # Get the current market price for the currency pair
        market_price = float(data['candles'][-1]['mid']['c'])
        #print(f"Market Price:", market_price)

        #DEBUG FORCE CODE
        #return "BUY"

        # Determine whether the market is trending up or down based on the moving averages
        if ma10 > ma20 > ma50 and market_price > ma10  and current_rsi > 30 and current_rsi < self.lower_rsi :
            # The market is trending up and the current price is above the 5-candle moving average and RSI is ok, so execute a "BUY"
            print("BUY")
            return "BUY"
        elif ma5 < ma20 < ma50 and market_price < ma5 and current_rsi < 70 and current_rsi < self.upper_rsi :
            # The market is trending down and the current price is below the 5-candle moving average and RSI is ok, so execute a "SELL"
            print("SELL")
            return "SELL"
        else:
            # The market is not trending or the current price is between the moving averages, so do not execute a trade
            print("NO ACTION")
            return "NO ACTION"
        
class TrendingStrategy3:        
    def __init__(self, settings):
        self.upper_rsi = settings['upper_rsi']
        self.lower_rsi = settings['lower_rsi']
        
    def decide(self, data):
        global ma5, ma10, ma20, ma50, ma100, current_rsi

        # Get the current market price for the currency pair
        market_price = float(data['candles'][-1]['mid']['c'])
        #print(f"Market Price:", market_price)

        #DEBUG FORCE CODE
        #return "BUY"

        # Determine whether the market is trending up or down based on the moving averages
        if ma20 > ma50 > ma100 and market_price > ma20 and  and current_rsi > 30 and current_rsi < self.lower_rsi :
            # The market is trending up and the current price is above the 20-candle moving average and RSI is ok, so execute a "BUY"
            print("BUY")
            return "BUY"
        elif ma20 < ma50 < ma100 and market_price < ma20 and current_rsi < 70 and current_rsi < self.upper_rsi :
            # The market is trending down and the current price is below the 20-candle moving average and RSI is ok, so execute a "SELL"
            print("SELL")
            return "SELL"
        else:
            # The market is not trending or the current price is between the moving averages, so do not execute a trade
            print("NO ACTION")
            return "NO ACTION"
        
class RangingStrategy1:
    def decide(self, data):
        # Code for identifying support and resistance levels and making a decision
        print("RangingStrategy1.decide executed")
        return "SELL"

class VolatileStrategy1:
    def decide(self, data):
        # Code for managing risk in volatile markets and making a decision
        print("VolatileStrategy1.decide executed")
        return "BUY"

class LowVolatilityStrategy1:
    def decide(self, data):
        # Code for identifying the trend and making a decision
        print("LowVolatilityStrategy1.decide executed")
        return "BUY"

class HighLiquidityStrategy1:
    def decide(self, data):
        # Code for identifying support and resistance levels and making a decision
        print("HighLiquidityStrategy1.decide executed")
        return "SELL"

class LowLiquidityStrategy1:
    def decide(self, data):
        # Code for managing risk in volatile markets and making a decision
        print("LowLiquidityStrategy1.decide executed")
        return "BUY"

class FundamentalStrategy1:
    def decide(self, data):
        # Code for identifying the trend and making a decision
        print("FundamentalStrategy.decide executed")
        return "BUY"

class TechnicalStrategy1:
    def decide(self, data):
        # Code for identifying support and resistance levels and making a decision
        print("TechnicalStrategy.decide executed")
        return "SELL"

class SentimentStrategy1:
    def decide(self, data):
        # Code for managing risk in volatile markets and making a decision
        print("SentimentStrategy.decide executed")
        return "BUY"

class RegulatoryStrategy1:
    def decide(self, data):
        # Code for identifying a Regulatory market and making a decision
        print("RegulatoryStrategy.decide executed")
        return "BUY"

# Function to fetch Historical Data
def get_historical_data(pair, general_settings, granularity=None, count=None):
    if granularity is None:
        granularity = general_settings['candle_size']
    if count is None:
        count = general_settings['num_candles_to_fetch']

    try:
        params = {"granularity": granularity, "count": count}
        request = instruments.InstrumentsCandles(instrument=pair, params=params)
        api.request(request)
        #print (request.response)
        return request.response
    except Exception as e:
        print(f"Fetch Error Occurred in get_historical_data: {e}")
    return

#Relative Strength Indicator
def rsi(data, period=14):
    delta = data['Close'].diff()
    gain, loss = delta.copy(), delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.abs().rolling(window=period).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# Function to process data and calculate moving averages and RSI
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

    # Calculate RSI
    data['RSI'] = rsi(data)
    
        # Assign the most recent moving average and RSI values to global variables
    # ... (same as before)
    
    
    # Assign the most recent moving average values to global variables
    global current_price 
    global ma5 
    global ma10 
    global ma20
    global ma50 
    global ma100
    global current_rsi
   
    current_price = round(float(data['MA5'].iloc[-1]),4)
    ma5 = round(float(data['MA5'].iloc[-1]),4)
    ma10 = round(float(data['MA10'].iloc[-1]),4)
    ma20 = round(float(data['MA20'].iloc[-1]),4)
    ma50 = round(float(data['MA50'].iloc[-1]),4)
    ma100 = round(float(data['MA100'].iloc[-1]),4)
    current_rsi = round(float(data['RSI'].iloc[-1]), 4)
    
    return data

# Function to analyze market conditions and select the best trading strategy
def select_strategy(pair, pair_data):
    # Analyze the data and choose the best strategy from the 10 strategies
    # This will require implementing the analysis logic based on the strategies mentioned above
    # Code required ...

    # else use the strategy in the config.ini file. Default is "TrendingStrategy1"
    # Check if the pair exists in the currency_pairs dictionary
    if pair in currency_pairs:
        # Return the strategy value from the dictionary
        return currency_pairs[pair]['strategy']
    else:
        # If the pair is not found in the dictionary, return a default strategy value
        return "TrendingStrategy1"

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

def execute_trade(pair_settings, decision, general_settings, default_currency_settings, currency_pairs):
    pair = pair_settings['pair']
    
    # Include Global Flags in this function to limit how many orders are placed for each currency pair.
    for currency_key in currency_pairs:
        if currency_pairs[currency_key] == pair_settings:
            tagname_expiry_flag = currency_key + "_flag"
            tagname_expiry_time = currency_key + "_flag_expiry_time"
            break

    # If the expiry flag is set, then do not execute this function
    if globals()[pair + "_flag"] == True:
        print("Expiry Flag True - Order can not be placed until:",globals()[tagname_expiry_time])
        return

    # Define Stop Loss Distance and Take Profit Distance
    round_decimals = 3 if pair in ["USD_JPY", "EUR_JPY", "GBP_JPY"] else 5
    stop_loss_distance = round((default_currency_settings['stop_loss_distance'] * pair_settings['scaling']), round_decimals)
    take_profit_distance = round((default_currency_settings['take_profit_distance'] * pair_settings['scaling']), round_decimals)

    # Define the opportunity to buy window
    buy_below_distance = round((default_currency_settings['buy_below_distance'] * pair_settings['scaling']), round_decimals)
    buy_above_distance = round((default_currency_settings['buy_above_distance'] * pair_settings['scaling']), round_decimals)

    # Calculate the trade size based on 0.5% of the total account value * margin 50:1
    account_value = get_account_value()
    trade_value = account_value * general_settings['trade_size'] * general_settings['account_margin']

    # fetch the current price of the currency pair
    ticker = get_historical_data(pair, general_settings ,granularity="S5", count=1)['candles'][0]['mid']['c']
    print(f"5S Candle Updated Price of {pair}: {ticker}")

    trade_quantity = math.floor(trade_value / float(ticker))

    # set the price that a buy/sell will occur
    if decision == "BUY":
         opportunity_price = round(float(ticker)  - buy_below_distance, round_decimals) # set to x pips below current price for a BUY
    elif decision == "SELL":
        opportunity_price = round(float(ticker)  + buy_above_distance, round_decimals) # set to x pips above current price for a SELL
    else :
        opportunity_price = 0 # set to 0 for NO ACTION

    # Set expiry time in UTC
    expiry_time_utc = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)

    # Convert expiry time to AEST timezone
    tz_aest = pytz.timezone('Australia/Sydney')
    expiry_time_aest = expiry_time_utc.astimezone(tz_aest)

    # Format expiry time as string in the expected format
    expiry_time_str = expiry_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Once the trade is executed, set the corresponding flag to True
    globals()[tagname_expiry_flag] = True

    # Once the trade is executed, set the corresponding flag_expiry_time
    globals()[tagname_expiry_time] = expiry_time_aest

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
                "price": str(round(opportunity_price, round_decimals)),
                "instrument": pair,
                "timeInForce": "GTD",
                "type": "LIMIT",
                "gtdTime": expiry_time_str,
                "positionFill": "DEFAULT",
                "takeProfitOnFill": {
                     "price": str(round((opportunity_price + take_profit_distance), round_decimals)) if decision == "BUY" else str(round((opportunity_price - take_profit_distance), round_decimals)),
                     "timeInForce": "GTC" 
                },
                "trailingStopLossOnFill": {
                    "distance": str(round(stop_loss_distance, round_decimals)),
                    "timeInForce": "GTC",
                    "type": "TRAILING_STOP_LOSS"
                }
            }
        }


    # Define a function to set the flag back to False when the expiry time is reached

        try:
            request = orders.OrderCreate(account_id, data=order_data)
            api.request(request)
            response = request.response
            print(f"{decision} order placed for {pair}, quantity: {trade_quantity} units at opportunity price:{opportunity_price} with stop loss:{stop_loss_distance}  to expire {expiry_time_str} ")
        except Exception as e:
            print(f"ORDER ERROR: {decision} order placed for {pair}, quantity: {trade_quantity} units at opportunity price:{opportunity_price} with stop loss:{stop_loss_distance}  to expire {expiry_time_str} ")
            print(f"Request Order Error Occurred in execute_trade: {e}")
    else:
        print(f"Insufficient account value to place {decision} order for {pair}")

def example_function(gen_parameter1, default_currency_settings, currency_pairs):
    # Print a single general value 
    print("Single gen_parameter1:",general_settings['gen_parameter1'])     

    # Print a single value from the default_currency_settings dictionary
    print("OrderType:", default_currency_settings['OrderType'])
    print("parameter1:",default_currency_settings['parameter1'])

    # Print a single value from the currency_pairs dictionary
    print("\nEUR_USD scaling:", currency_pairs['EUR_USD']['scaling'])
    print("pair:",currency_pairs['EUR_USD']['pair'],"\n")
    
    # Iterate through currency_pairs and print pair values
    for currency_pair, settings in currency_pairs.items():
        print(f"{currency_pair} pair:", settings['pair'])

    # Print All Values from Dictionaries
    print("\nAll General Settings:", general_settings)
    print("\nAll Default currency settings:", default_currency_settings)
    print("All Currency Pair Data:", currency_pairs)

# Main function
def main(general_settings, default_currency_settings, currency_pairs):
    for pair in currency_pairs:
        #DEBUG 6 
        #print("EUR_USD Expiry Flag:",EUR_USD_flag)
        #print("EUR_USD Expiry Time:",EUR_USD_flag_expiry_time)
        #print("AUD_USD Expiry Flag:",AUD_USD_flag)
        #print("AUD_USD Expiry Time:",AUD_USD_flag_expiry_time)

        pair_data = get_historical_data(pair, general_settings)

        # Process the data and calculate moving averages
        if pair_data is None:
            print("Error fetching historical data.")
            return

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

        # Initialize strategy objects
        trending_strategy1 = TrendingStrategy1(default_currency_settings)
        trending_strategy2 = TrendingStrategy2(default_currency_settings)
        trending_strategy3 = TrendingStrategy3(default_currency_settings)
        ranging_strategy1 = RangingStrategy1()
        volatile_strategy1 = VolatileStrategy1()
        low_volatility_strategy1 = LowVolatilityStrategy1()
        high_liquidity_strategy1 = HighLiquidityStrategy1()
        low_liquidity_strategy1 = LowLiquidityStrategy1()
        fundamental_strategy1 = FundamentalStrategy1()
        technical_strategy1 = TechnicalStrategy1()
        sentiment_strategy1 = SentimentStrategy1()
        regulatory_strategy1 = RegulatoryStrategy1()

        #initialise decision variable
        decision = None

        # Execute the selected strategy
        if strategy == "TrendingStrategy1":
            decision = trending_strategy1.decide(pair_data)
        elif strategy == "TrendingStrategy2":
            decision = trending_strategy2.decide(pair_data)
        elif strategy == "TrendingStrategy3":
            decision = trending_strategy3.decide(pair_data)
        elif strategy == "RangingStrategy1":
            decision = ranging_strategy1.decide(pair_data)
        elif strategy == "VolatileStrategy1":
            decision = volatile_strategy1.decide(pair_data)
        elif strategy == "LowVolatilityStrategy1":
            decision = low_volatility_strategy1.decide(pair_data)
        elif strategy == "HighLiquidityStrategy1":
            decision = high_liquidity_strategy1.decide(pair_data)
        elif strategy == "LowLiquidityStrategy1":
            decision = low_liquidity_strategy1.decide(pair_data)
        elif strategy == "FundamentalStrategy1":
            decision = fundamental_strategy1.decide(pair_data)
        elif strategy == "TechnicalStrategy1":
            decision = technical_strategy1.decide(pair_data)
        elif strategy == "SentimentStrategy1":
            decision = sentiment_strategy1.decide(pair_data)
        elif strategy == "RegulatoryStrategy1":
            decision = regulatory_strategy1.decide(pair_data)

        # Call get_account_value() and execute_trade() if the decision is "BUY" or "SELL"
        if decision in ["BUY","SELL"]:
            print("Account Value:", get_account_value())
            execute_trade(currency_pairs[pair], decision, general_settings, default_currency_settings, currency_pairs)


#if __name__ == "__main__":
#    main()

while True:

    # Read config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # General settings as a dictionary
    general_settings = {
        'access_token': config.get('general', 'access_token'),
        'account_id': config.get('general', 'account_id'),
        'account_margin': float(config.get('general', 'account_margin')),
        'trade_size': float(config.get('general', 'trade_size')),
        'candle_size': config.get('general', 'candle_size'),
        'num_candles_to_fetch': int(config.get('general', 'num_candles_to_fetch')),
        'gen_parameter1': float(config.get('general', 'gen_parameter1')),
        'gen_parameter2': float(config.get('general', 'gen_parameter2')),
        'gen_parameter3': float(config.get('general', 'gen_parameter3')),
        'gen_parameter4': float(config.get('general', 'gen_parameter4')),
        'gen_parameter5': float(config.get('general', 'gen_parameter5')),
        'gen_parameter6': float(config.get('general', 'gen_parameter6')),
}

    # Default currency settings
    default_currency_settings = {
        'scaling': float(config.get('default_currency_settings', 'scaling')),
        'OrderType': config.get('default_currency_settings', 'OrderType'),
        'TimeInForce': config.get('default_currency_settings', 'TimeInForce'),
        'TakeProfitOnFill_TimeInForce': config.get('default_currency_settings', 'TakeProfitOnFill_TimeInForce'),
        'TrailingStopLossOnFill_TimeInForce': config.get('default_currency_settings', 'TrailingStopLossOnFill_TimeInForce'),
        'stop_loss_distance': float(config.get('default_currency_settings', 'stop_loss_distance')),
        'take_profit_distance': float(config.get('default_currency_settings', 'take_profit_distance')),
        'buy_below_distance': float(config.get('default_currency_settings', 'buy_below_distance')),
        'buy_above_distance': float(config.get('default_currency_settings', 'buy_above_distance')),
        'lower_rsi': float(config.get('default_currency_settings', 'lower_rsi')),
        'upper_rsi': float(config.get('default_currency_settings', 'upper_rsi')),
        'parameter1': float(config.get('default_currency_settings', 'parameter1')),
        'parameter2': float(config.get('default_currency_settings', 'parameter2')),
        'parameter3': float(config.get('default_currency_settings', 'parameter3')),
        'parameter4': float(config.get('default_currency_settings', 'parameter4')),
        'parameter5': float(config.get('default_currency_settings', 'parameter5')),
        'parameter6': float(config.get('default_currency_settings', 'parameter6')),
    }

    # Currency Pair Data
    currency_pairs = {}
    for section in config.sections():
        if section != 'general' and section != 'default_currency_settings':
            currency_pairs[section] = {
                'pair': config.get(section, 'pair'),
                'scaling': float(config.get(section, 'scaling')),
                'strategy': config.get(section, 'strategy')
            }

    # Create global flag variables for each currency pair
    if is_first_scan:
        for currency in currency_pairs:
            globals()[currency + "_flag"] = False
            globals()[currency + "_flag_expiry_time"] = 0

    # Initialize API connection
    access_token = general_settings['access_token']
    account_id = general_settings['account_id']
    api = API(access_token=access_token)

    # Now you can use the config values

    # Call the example function with the dictionaries as arguments
    #example_function(general_settings, default_currency_settings, currency_pairs)
    
    #Call Main Function
    main(general_settings, default_currency_settings, currency_pairs)
    
    # After the first scan is complete, set is_first_scan to False
    if is_first_scan:
        is_first_scan = False

    time.sleep(30) # Pause the while loop for 30 seconds

