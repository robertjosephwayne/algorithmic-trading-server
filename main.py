import os
import urllib.parse
from flask import Flask, request
from flask_cors import CORS
from alpaca.data.live import CryptoDataStream
from alpaca_trade_api.rest import TimeFrame, URL, REST, TimeFrameUnit
from dotenv import load_dotenv
import threading
from flask_socketio import SocketIO

load_dotenv()

API_KEY = os.environ.get('ALPACA_API_KEY')
SECRET_KEY = os.environ.get('ALPACA_API_SECRET')
CLIENT_URL = os.environ.get('CLIENT_URL')

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app=app, cors_allowed_origins="*")


@app.route("/api/crypto/bars/<symbol>")
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


base_url = URL("https://paper-api.alpaca.markets")
data_feed = "sip"
rest = REST(key_id=API_KEY, secret_key=SECRET_KEY, base_url=base_url)
crypto_stream = CryptoDataStream(api_key=API_KEY, secret_key=SECRET_KEY)


async def handle_crypto_bar(bar):
    bar = {
        "symbol": bar.symbol,
        "price": bar.price
    }
    socketio.emit('bar', bar)


def start_crypto_stream():
    crypto_stream.subscribe_trades(handle_crypto_bar, "BTC/USD", "ETH/USD", "LTC/USD")
    crypto_stream.run()


threading.Thread(target=start_crypto_stream).start()

if __name__ == '__main__':
    socketio.run(app)



