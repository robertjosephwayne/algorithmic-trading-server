from threading import Thread
from alpaca.data.live import CryptoDataStream
from alpaca_trade_api.rest import URL
from config import config

trading_mode = "PAPER"
if config["ALPACA"]["ENABLE_LIVE_TRADING"]:
    trading_mode = "LIVE"

base_url = URL(config["ALPACA"][trading_mode]["ENDPOINT"])
api_key = config["ALPACA"][trading_mode]["API_KEY"]
secret_key = config["ALPACA"][trading_mode]["SECRET_KEY"]
data_feed = "sip"


class AlpacaWebSocketClient:
    _base_url = base_url

    def __init__(self):
        super().__init__()
        self._handle_trade = None
        self._crypto_stream = CryptoDataStream(api_key=api_key, secret_key=secret_key)

    def _run_websocket(self):
        print("Connecting to Alpaca websocket...")
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
