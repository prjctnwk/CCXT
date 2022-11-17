import ccxt
import pandas as pd
import numpy as np


ticker = 'BTCUSDT' #future = 'BTCUSDT', spot = 'BTC/USDT' 
timeframe = '1m'
limit = 4320 #3 days

exchange = ccxt.binanceusdm({
    'apiKey' : '' ,
    'secret' : '' , 
    'enableRateLimit' : True ,
    'options' : {
        'defaultType' : 'future',
     },
})


#GET CANDLE DF OF THE LAST N CANDE (N=LIMIT)
#def getdata(exchange, ticker, timeframe, limit)
    #df = pd.DataFrame(exchange.fetch_ohlcv(ticker, timeframe, limit=limit), \
        #columns=['time', 'open', 'high', 'low', 'close', 'volume']).set_index('time')
            #return df



candle = exchange.fetch_ohlcv(ticker, timeframe, limit=limit), \
df = pd.DataFrame(candle, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']).set_index('time')
df['timestamp'] = pd.to_datetime(df.['timestamp'], unit = 'ms')

#THRESHOLD
spike_up_threshold = 0.2
spike_down_threshold = -0.2
volume_threshold = 1900 #volume in Bitcoin
previous_volume_threshold= 900
atr_threshold = 110
atr_window = 14


CloseOpen = round((df.close - df.open),2)
Color = list(map(lambda x: "black" if x <= 0 else "white", CloseOpen))
higher = df.high.rolling(15).max()
lower = df.low.rolling(15).min()
Range = round(df.high - df.low, 2)
Body = abs(df.open - df.close,)
CO = round(df.close - df.open, 2)
OL = round(df.open - df.low, 2)
HO round(df.high - df.open, 2)
LC = round(df.low - df.close, 2)
HC = round(df.high - df.close, 2)
BodyPerc = (df.close - df.open) / df.close * 100

#AVERAGE PRICE
def avgprice(O,C,L,H):
    avg = ((O + C + L + H) / 4)
    return avg
avg = avgprice(df.open, df.low, df.close, df.high)

#AVERAGE TRUE RANGE
def atr():
    df2 = pd.concat([Range, HC, LC] , axis = 1)
    TrueRange = np.max(df2, axis = 1)
    atr = TrueRange.rolling(atr_window).mean()
    return atr

df["atr"] = atr()


#SET SPIKE
SpikeDownBlack = ((((df.low - df.close) / df.close) * 100))
SpikeDownWhite = ((((df.low - df.open) / df.open) *100))
df["spikeDown"] = np.where((Color == "black"), SpikeDownBlack, SpikeDownWhite)

SpikeUpBlack = ((((df.high - df.open) / df.open) * 100))
SpikeUpWhite = ((((df.high - df.close) / df.close) * 100))
df["spikeUp"] = np.where((Color == "black"), SpikeUpBlack, SpikeUpWhite)
                     
# ASSIGN TRUE OR FALSE TO THE VALUES 
df["SpikeUp_TF"] = np.where((df.spikeUp.shift(1) > spike_up_threshold) & (df.spikeDown.shift(1) > -0.04) & 
                              (df.spikeUp.shift(1) < (0.59)), 1,0)

df["SpikeDown_TF"] = np.where((df.spikeDown.shift(1) <= spike_down_threshold) & (df.spikeUp.shift(1) < 0.04) &
                                (df.spikeDown.shift(1) > (-0.59)), 1,0)
                               
df["Volume_TF"] = np.where((df.volume.shift(1) > volume_threshold) & 
                            (df.volume.shift(2) < previous_volume_threshold), 1,0)


#ENTRY CONDITIONS
conditionlist = [
((df["Volume_TF"] == 1) & (df["SpikeUp_TF"] == 1) & (df["BodyPerc"] <= 0.29) & (BodyPerc >= -0.1) &
(df["atr"] < atr_threshold)) , 
((df["Volume_TF"] == 1) & (df["SpikeDown_TF"] == 1) & (BodyPerc >= -0.29) & (BodyPerc <= 0.1) &
(df["atr"] < atr_threshold)) , 
((df["Volume_TF"] == 1) & (df["SpikeDown_TF"] == 1) & (df["SpikeUp_TF"] == 1))] 
choicelist = [2, 1, 0] # 2 = Short, 1 = long, 0 = /
df["open_position"] = np.select(conditionlist, choicelist, default=0)
