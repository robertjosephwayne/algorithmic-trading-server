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

    def start_crypto_stream(self):
        self._crypto_stream.subscribe_trades(self._handle_trade, "BTC/USD", "ETH/USD", "LTC/USD")
        self._crypto_stream.run()

    def set_handle_trade(self, handler):
        self._handle_trade = handler


