import vectorbtpro as vbt
import numpy as np
import pandas as pd
from config import config

vbt.settings.data["custom"]["alpaca"]["client_config"]["api_key"] = config["ALPACA"]["LIVE"]["API_KEY"]
vbt.settings.data["custom"]["alpaca"]["client_config"]["secret_key"] = config["ALPACA"]["LIVE"]["SECRET_KEY"]

symbol = 'ETHUSD'
start = '30 days ago UTC'
limit = 5000

# vbt.AlpacaData.set_custom_settings(
#     client_config=dict(
#         api_key=config["ALPACA"]["BACKTEST"]["API_KEY"],
#         secret_key=config["ALPACA"]["BACKTEST"]["SECRET_KEY"],
#         paper=False
#     )
# )

vbt.AlpacaData.fetch(symbols=symbol, start=start, timeframe="1 hour").get()
# vbt.AlpacaData.
# print(data)
# print(data.get("Close"))

# alpaca_data = vbt.AlpacaData.download(symbol, start=start, end=end, timeframe=timeframe, exchange="CBSE").get('Close')
#
# fast_ma = vbt.MA.run(alpaca_data, 12, short_name='fast')
# slow_ma = vbt.MA.run(alpaca_data, 24, short_name='slow')
#
# entries = fast_ma.ma_crossed_above(slow_ma)
# exits = fast_ma.ma_crossed_below(slow_ma)
#
# pf = vbt.Portfolio.from_signals(alpaca_data, entries, exits)
#
# total_return = pf.total_return()
# print("Total Return: ", total_return)