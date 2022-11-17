import pandas as pd
import ccxt
import pandas_ta as ta
import math
import time
import dontshare_config as ds


ticker = 'BTCUSDT' #future non va la barra(BTCUSDT), spot si (BTC/USDT) 

exchange = ccxt.binanceusdm({
    'apiKey' : '' ,
    'secret' : '' , 
    'enableRateLimit' : True ,
    'options' : {
        'defaultType' : 'future',
     },
})

#ALL MARKET
markets = exchange.load_markets()

#ASK BALANCE
#balance = client.get_asset_balance(asset = 'USDT')
balance = exchange.fetch_balance()
