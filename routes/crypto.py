import os
from flask import Blueprint, request
import urllib.parse
from alpaca_trade_api.rest import TimeFrame, URL, REST, TimeFrameUnit
from dotenv import load_dotenv

load_dotenv()

crypto_blueprint = Blueprint('crypto', __name__)

API_KEY = os.environ.get('ALPACA_API_KEY')
SECRET_KEY = os.environ.get('ALPACA_API_SECRET')
CLIENT_URL = os.environ.get('CLIENT_URL')

base_url = URL("https://paper-api.alpaca.markets")
data_feed = "sip"
rest = REST(key_id=API_KEY, secret_key=SECRET_KEY, base_url=base_url)


@crypto_blueprint.route("/api/crypto/bars/<symbol>")
def get_crypto_bars(symbol):
    timeframe = request.args.get("timeframe")

    encoded_start = request.args.get("start")
    start = urllib.parse.unquote(encoded_start)

    alpaca_timeframe = None
    match timeframe:
        case 'minute':
            alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Minute)
        case 'hour':
            alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Hour)
        case 'day':
            alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Day)
        case 'week':
            alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Week)
        case 'month':
            alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Month)

    bars = rest.get_crypto_bars(symbol, alpaca_timeframe, start)

    response = list()

    for bar in bars:
        response.append({
            "symbol": symbol,
            "timestamp": bar.t,
            "high": bar.h,
            "low": bar.l,
            "open": bar.o,
            "close": bar.c
        })

    return response


@crypto_blueprint.route("/api/crypto/trades/latest")
def get_latest_crypto_trades():
    supported_tickers = ["BTCUSD", "ETHUSD", "LTCUSD"]
    result = rest.get_latest_crypto_trades(supported_tickers, "CBSE")

    response = {}

    for ticker in supported_tickers:
        trade = result[ticker]
        response[ticker] = {
            "price": trade.price,
            "timestamp": trade.timestamp,
            "exchange": trade.x
        }

    return response
