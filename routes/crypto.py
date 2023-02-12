from flask import Blueprint, request
import urllib.parse
from alpaca_trade_api.rest import TimeFrame, URL, REST, TimeFrameUnit
from config import config

crypto_blueprint = Blueprint('crypto', __name__)

base_url = URL("https://paper-api.alpaca.markets")
data_feed = "sip"
rest = REST(key_id=config["ALPACA"]["API_KEY"], secret_key=config["ALPACA"]["SECRET_KEY"], base_url=base_url)
supported_tickers = ["BTCUSD", "ETHUSD", "LTCUSD"]


@crypto_blueprint.route("/bars/<symbol>")
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

    bars = rest.get_crypto_bars(symbol, alpaca_timeframe, start, limit=60, exchanges=['CBSE'])

    response = list()

    for bar in bars:
        response.append({
            "symbol": symbol,
            "timestamp": bar.t,
            "high": bar.h,
            "low": bar.l,
            "open": bar.o,
            "close": bar.c,
            "exchange": bar.x
        })

    return response


@crypto_blueprint.route("/bars/latest")
def get_latest_crypto_bars():
    result = rest.get_latest_crypto_bars(supported_tickers, "CBSE")

    response = {}

    for ticker in supported_tickers:
        bar = result[ticker]
        response[ticker] = {
            "high": bar.h,
            "low": bar.l,
            "open": bar.o,
            "close": bar.c,
            "timestamp": bar.t,
            "volume": bar.v,
            "weighted_volume": bar.vw,
            "exchange": bar.x
        }

    return response


@crypto_blueprint.route("/trades/latest")
def get_latest_crypto_trades():
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
