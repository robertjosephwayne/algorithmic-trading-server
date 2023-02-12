from alpaca.data.live import CryptoDataStream
from alpaca_trade_api.rest import URL


class AlpacaWebSocketClient:
    _base_url = URL("https://paper-api.alpaca.markets")

    def __init__(self, api_key, api_secret):
        super().__init__()
        self._api_key = api_key
        self._api_secret = api_secret
        self._handle_trade = None
        self._crypto_stream = CryptoDataStream(api_key=api_key, secret_key=api_secret)

    def subscribe_trades(self, tickers, handler):
        self._crypto_stream.subscribe_trades(handler, *tickers)

    def start_stream(self):
        self._crypto_stream.run()


