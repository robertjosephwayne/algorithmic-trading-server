import sys
import os
import time
import pandas as pd
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import vectorbtpro as vbt
from config import config
from itertools import product

API_KEY = config["ALPACA"]["LIVE"]["API_KEY"]
SECRET_KEY = config["ALPACA"]["LIVE"]["SECRET_KEY"]

client_type = "crypto"

vbt.AlpacaData.set_custom_settings(
    client_type=client_type, client_config=dict(api_key=API_KEY, secret_key=SECRET_KEY,)
)


def run(data, slow_periods, fast_periods):
    fast_ma = vbt.MA.run(data, fast_periods, short_name="fast")
    slow_ma = vbt.MA.run(data, slow_periods, short_name="slow")

    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)

    pf = vbt.Portfolio.from_signals(data, entries, exits)
    return pf.stats([
        "total_return",
        "total_trades",
        "win_rate",
        "expectancy"
    ])


symbol = "BTC/USD"
start = "2019-01-01 UTC"
end = "1 hour ago UTC"
timeframe = "1 hour"

slow_periods = range(100, 200)
fast_periods = range(1, 100)

period_combs = list(product(slow_periods, fast_periods))
comb_count = len(period_combs)
print(f"Testing {comb_count} combinations.")
start = time.time()

alpaca_data = vbt.AlpacaData.fetch(
    symbols=symbol, start=start, end=end, timeframe=timeframe
).get("Close")

comb_stats = [
    run(data=alpaca_data, slow_periods=slow_periods, fast_periods=fast_periods)
    for slow_periods, fast_periods in period_combs
]

comb_stats_df = pd.DataFrame(comb_stats)
print(comb_stats_df)

comb_stats_df.index = pd.MultiIndex.from_tuples(period_combs, names=['fast_periods', 'slow_periods'])
print(comb_stats_df)

comb_stats_df['Expectancy'].vbt.heatmap().show()
end = time.time()
print(f"Time elapsed: {end - start}")