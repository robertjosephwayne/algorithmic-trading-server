from threading import Thread
from alpaca.data.live import CryptoDataStream
from alpaca_trade_api.rest import URL
from config import config

base_url = URL("https://paper-api.alpaca.markets")
api_key = config["ALPACA"]["PAPER"]["API_KEY"]
secret_key = config["ALPACA"]["PAPER"]["SECRET_KEY"]
data_feed = "sip"

if config["ALPACA"]["ENABLE_LIVE_TRADING"]:
    base_url = URL("https://api.alpaca.markets")
    api_key = config["ALPACA"]["LIVE"]["API_KEY"]
    secret_key = config["ALPACA"]["LIVE"]["SECRET_KEY"]

class AlpacaWebSocketClient:
    _base_url = base_url

    def __init__(self):
        super().__init__()
        self._handle_trade = None
        self._crypto_stream = CryptoDataStream(api_key=api_key, secret_key=secret_key)

    def _run_websocket(self):
        self._crypto_stream.run()

    def subscribe_trades(self, tickers, handler):
        self._crypto_stream.subscribe_trades(handler, *tickers)

    def subscribe_quotes(self, tickers, handler):
        self._crypto_stream.subscribe_quotes(handler, *tickers)

    def subscribe_bars(self, tickers, handler):
        self._crypto_stream.subscribe_bars(handler, *tickers)

    def connect(self):
        websocket_thread = Thread(target=self._run_websocket)
        websocket_thread.daemon = True
        websocket_thread.start()
