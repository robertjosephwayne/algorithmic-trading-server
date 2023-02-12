from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import threading
from connectors.alpaca.websocket.client import AlpacaWebSocketClient
from routes.crypto import crypto_blueprint
from config import config


app = Flask(__name__)
app.register_blueprint(crypto_blueprint, url_prefix='/api/crypto')
CORS(app)
socketio = SocketIO(app=app, cors_allowed_origins="*")


async def handle_crypto_bar(bar):
    bar = {
        "symbol": bar.symbol,
        "price": bar.price
    }
    socketio.emit('bar', bar)


alpaca = AlpacaWebSocketClient(
    api_key=config["ALPACA"]["API_KEY"],
    api_secret=config["ALPACA"]["SECRET_KEY"]
)
alpaca.set_handle_trade(handle_crypto_bar)
threading.Thread(target=alpaca.start_crypto_stream).start()

if __name__ == '__main__':
    socketio.run(app)



