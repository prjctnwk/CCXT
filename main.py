import ccxt
import time
import pandas as pd
import numpy as np
from datetime import date, datetime
from functions import exchange, balance
from getdata import df

ticker = 'BTCUSDT' #future = 'BTCUSDT, spot = 'BTC/USDT' 
timeframe = '1m'
limit = 4320 #3 days
tp_perc = 0.01
sl_perc = 0.005
margin = 100 #$
leverage= 100


#GET BID AND ASK ON ORDER BOOK
def get_bid_ask():

    book = exchange.fetch_order_book(ticker)
    bid = book['bids'] [0] [0]
    ask = book['asks'] [0] [0]
    print (f'best bid:{bid} best ask: {ask}')
    return bid, ask

mybid = get_bid_ask()[0]
myask = get_bid_ask()[1]

params= {'timeInForce' : 'PostOnly'}

quantity= = ((margin * leverage) / df.open).apply(lambda x: round(x,6)) #qtà in btc

#SET POSITION SIZE
#def positionsize(ticker, margin):
    #return round(ticker/exchange.fetch_ticker(ticker)['last'],3)
    #return round(100/exchange.fetch_ticker(symbol+ '/USDT')['last'],3)

#SET THE PERCENTAGE OF FRACTION FOR EACH POSITION
#portion_balance = float(balance['free']) * 0.10

def buymarket(symbol, qty, sl, tp):
    exchange.create_market_buy_order(ticker, quantity, sl, tp)


def sellmarket(symbol, qty, sl, tp):
    exchange.create_market_sell_order(ticker, quantity, sl, tp)

def buylimit(symbol, qty, sl, tp):
    exchange.create_limit_buy_order(ticker, quantity, params, sl, tp)


def selllimit(symbol, qty, sl, tp):
    exchange.create_limit_sell_order(ticker, quantity, params, sl, tp)

#set sl e tp
entryprice = np.where((df.openposition ==1 | df.openposition == 2), open, 0))

stoploss = entry * (1-(sl_perc/100))
takeprofit = entry * (1+(tp_perc/100))


#open positions
while True:
    if df.open_position == 1:
        buymarket(ticker, quantity, stoploss, takeprofit)
        time.sleep(0.5)


    if df.open_position == 2:
        
        sellmarket(ticker, quantity, stoploss, takeprofit)
        time.sleep(0.5)