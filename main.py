from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from alpaca.data.live import CryptoDataStream
from alpaca_trade_api.rest import URL
from config import config
import threading
from routes.crypto import crypto_blueprint


app = Flask(__name__)
app.register_blueprint(crypto_blueprint, url_prefix='/api/crypto')
CORS(app)
socketio = SocketIO(app=app, cors_allowed_origins="*")

base_url = URL("https://paper-api.alpaca.markets")
data_feed = "sip"
crypto_stream = CryptoDataStream(api_key=config["ALPACA"]["API_KEY"], secret_key=config["ALPACA"]["SECRET_KEY"])


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



