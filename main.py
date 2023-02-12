import os
from flask import Flask, request
from flask_cors import CORS
from alpaca.data.live import CryptoDataStream
from alpaca_trade_api.rest import TimeFrame, URL, REST, TimeFrameUnit
from dotenv import load_dotenv
import threading
from flask_socketio import SocketIO
from routes.crypto import crypto_blueprint

load_dotenv()

API_KEY = os.environ.get('ALPACA_API_KEY')
SECRET_KEY = os.environ.get('ALPACA_API_SECRET')
CLIENT_URL = os.environ.get('CLIENT_URL')

app = Flask(__name__)
app.register_blueprint(crypto_blueprint)
CORS(app)
socketio = SocketIO(app=app, cors_allowed_origins="*")

base_url = URL("https://paper-api.alpaca.markets")
data_feed = "sip"
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



