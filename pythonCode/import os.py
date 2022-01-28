import os 
from binance.client import Client
import pandas as pd 
import datetime as dt
from calendar import monthrange

api_key = os.environ.get('binance_api_key')
api_secret = os.environ.get('binance_secret')

# we initialize our client and pass through the API key and secret.
client = Client(api_key, api_secret)

timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1m')

bars = client.get_historical_klines('BTCUSDT', '5m', 1577892802000 , 1580571202000 , limit=1000)

print(len(bars))
