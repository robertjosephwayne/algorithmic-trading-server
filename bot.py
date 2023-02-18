from datetime import datetime, timedelta
import math
from config import config

from alpaca_trade_api.rest import TimeFrame, URL, REST
base_url = URL("https://paper-api.alpaca.markets")
data_feed = "sip"
rest = REST(key_id=config["ALPACA"]["API_KEY"], secret_key=config["ALPACA"]["SECRET_KEY"], base_url=base_url)

SMA_FAST = 12
SMA_SLOW = 24
QTY_PER_TRADE = 1


def get_position(symbol):
    positions = rest.list_positions()
    for p in positions:
        if p.symbol == symbol:
            return float(p.qty)
    return 0


def get_pause():
    now = datetime.now()
    next_min = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
    pause = math.ceil((next_min - now).seconds)
    return pause


def get_sma(series, periods):
    return series.rolling(periods).mean()


def get_signal(fast, slow):
    print(f"Fast {fast[-1]} / Slow: {slow[-1]}")
    return fast[-1] > slow[-1]


def get_bars(symbol):
    bars = rest.get_crypto_bars(symbol, TimeFrame.Minute, exchanges=["CBSE"]).df
    bars[f'sma_fast'] = get_sma(bars.close, SMA_FAST)
    bars[f'sma_slow'] = get_sma(bars.close, SMA_SLOW)
    return bars


async def process_bar(bar):
    symbol = bar.symbol.replace("/", "")

    bars = get_bars(symbol=symbol)

    position = get_position(symbol=symbol)
    should_buy = get_signal(bars.sma_fast, bars.sma_slow)

    if position == 0 and should_buy == True:
        qty = QTY_PER_TRADE
        print(f'Symbol: {symbol} / Side: BUY / Quantity: {qty}')
        rest.submit_order(symbol=symbol, qty=qty, side="buy", time_in_force="gtc")
    elif position > 0 and should_buy == False:
        qty = position
        print(f'Symbol: {symbol} / Side: SELL / Quantity: {qty}')
        rest.submit_order(symbol=symbol, qty=qty, side="sell", time_in_force="gtc")