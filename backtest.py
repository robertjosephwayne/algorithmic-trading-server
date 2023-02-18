import vectorbt as vbt
from config import config

vbt.settings.data["alpaca"]["key_id"] = config["ALPACA"]["API_KEY"]
vbt.settings.data["alpaca"]["secret_key"] = config["ALPACA"]["SECRET_KEY"]

symbol = 'BTCUSD'
start = '2022-01-01 UTC'
end = '1 minute ago UTC'
timeframe = '1m'

alpaca_data = vbt.AlpacaData.download(symbol, start=start, end=end, timeframe=timeframe, exchange="CBSE").get('Close')

fast_ma = vbt.MA.run(alpaca_data, 12, short_name='fast')
slow_ma = vbt.MA.run(alpaca_data, 24, short_name='slow')

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf = vbt.Portfolio.from_signals(alpaca_data, entries, exits)

total_return = pf.total_return()
print("Total Return: ", total_return)