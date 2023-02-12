from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from connectors.alpaca.websocket.client import AlpacaWebSocketClient
from routes.crypto import crypto_blueprint
from config import config


app = Flask(__name__)
app.register_blueprint(crypto_blueprint, url_prefix='/api/crypto')
CORS(app)
socketio = SocketIO(app=app, cors_allowed_origins="*")


async def handle_crypto_trade(trade):
    trade = {
        "symbol": trade.symbol,
        "price": trade.price
    }
    socketio.emit('bar', trade)


alpaca = AlpacaWebSocketClient(
    api_key=config["ALPACA"]["API_KEY"],
    api_secret=config["ALPACA"]["SECRET_KEY"]
)
alpaca.subscribe_trades(["BTC/USD", "ETH/USD", "LTC/USD"], handle_crypto_trade)
alpaca.connect()

if __name__ == '__main__':
    socketio.run(app)



