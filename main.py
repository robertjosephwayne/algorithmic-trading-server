import os
import urllib.parse
from flask import Flask, request
from flask_cors import CORS
from alpaca.data.timeframe import TimeFrame
from alpaca_trade_api.rest import TimeFrame, URL, REST
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get('ALPACA_API_KEY')
SECRET_KEY = os.environ.get('ALPACA_API_SECRET')

base_url = URL("https://paper-api.alpaca.markets")
feed = "sip"
rest = REST(key_id=API_KEY, secret_key=SECRET_KEY, base_url=base_url)


@app.route("/api/crypto/bars/<symbol>")
def get_crypto_bars(symbol):
    timeframe = request.args.get("timeframe")

    encoded_start = request.args.get("start")
    start = urllib.parse.unquote(encoded_start)

    alpaca_timeframe = None
    match timeframe:
        case 'minute':
            alpaca_timeframe = TimeFrame.Minute
        case 'hour':
            alpaca_timeframe = TimeFrame.Hour
        case 'day':
            alpaca_timeframe = TimeFrame.Day
        case 'week':
            alpaca_timeframe = TimeFrame.Week
        case 'month':
            alpaca_timeframe = TimeFrame.Month

    bars = rest.get_crypto_bars(symbol, alpaca_timeframe, start)

    response = list()

    for bar in bars:
        response.append({
            "Symbol": symbol,
            "Timestamp": bar.t,
            "High": bar.h,
            "Low": bar.l,
            "Open": bar.o,
            "Close": bar.c
        })

    return response


if __name__ == '__main__':
    app.run()
