import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import vectorbtpro as vbt
from config import config

API_KEY = config["ALPACA"]["LIVE"]["API_KEY"]
SECRET_KEY = config["ALPACA"]["LIVE"]["SECRET_KEY"]

symbol = "ETH/USD"
start = "2022-01-01 UTC"
end = "1 hour ago UTC"
timeframe = "1 hour"
client_type = "crypto"

vbt.AlpacaData.set_custom_settings(
    client_type=client_type, client_config=dict(api_key=API_KEY, secret_key=SECRET_KEY,)
)

alpaca_data = vbt.AlpacaData.fetch(
    symbols=symbol, start=start, end=end, timeframe=timeframe
).get("Close")

fast_ma = vbt.MA.run(alpaca_data, 12, short_name="fast")
slow_ma = vbt.MA.run(alpaca_data, 24, short_name="slow")

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf = vbt.Portfolio.from_signals(alpaca_data, entries, exits)
pf.plot().show()

total_return = pf.get_total_return()
print("Total Return: ", total_return)

market_return = pf.get_total_market_return()
print(market_return)
