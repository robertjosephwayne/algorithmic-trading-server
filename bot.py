from datetime import datetime, timedelta
from alpaca_trade_api.rest import TimeFrame
from connectors.alpaca.rest.client import alpaca_rest_client

SMA_FAST = 12 * 60
SMA_SLOW = 24 * 60
QTY_PER_TRADE = 1
USD_PER_TRADE = 100


def get_position(symbol):
    positions = alpaca_rest_client.list_positions()
    for p in positions:
        if p.symbol == symbol:
            return float(p.qty)
    return 0


def get_sma(series, periods):
    return series.rolling(periods).mean()


def get_signal(fast, slow):
    print(f"Fast {fast[-1]} / Slow: {slow[-1]}")
    return fast[-1] > slow[-1]


def get_bars(symbol):
    print(f"Bar Received: {symbol}")

    now = datetime.now()
    delta = timedelta(days=2)
    start = now - delta

    bars = alpaca_rest_client.get_crypto_bars(symbol, TimeFrame.Minute, exchanges=["CBSE"], start=start.strftime("%Y-%m-%d")).df

    bars[f"sma_fast"] = get_sma(bars.close, SMA_FAST)
    bars[f"sma_slow"] = get_sma(bars.close, SMA_SLOW)
    return bars


async def process_bar(bar):
    symbol = bar.symbol.replace("/", "")

    bars = get_bars(symbol=symbol)

    position = get_position(symbol=symbol)
    should_buy = get_signal(bars.sma_fast, bars.sma_slow)

    if position == 0 and should_buy == True:
        print(f"Symbol: {symbol} / Side: BUY / Notional Amount: {USD_PER_TRADE}")
        alpaca_rest_client.submit_order(
            symbol=symbol, notional=USD_PER_TRADE, side="buy", time_in_force="gtc"
        )
    elif position > 0 and should_buy == False:
        print(f"Symbol: {symbol} / Side: SELL / Quantity: {position}")
        alpaca_rest_client.submit_order(symbol=symbol, qty=position, side="sell", time_in_force="gtc")
