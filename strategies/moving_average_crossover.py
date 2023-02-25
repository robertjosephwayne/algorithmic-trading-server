import math
from datetime import datetime, timedelta
from alpaca_trade_api.rest import TimeFrame
from connectors.alpaca.rest.client import alpaca_rest_client


class MovingAverageCrossoverStrategy:
    def __init__(self, sma_fast_hours, sma_slow_hours):
        super().__init__()
        self._sma_fast_hours = sma_fast_hours
        self._sma_slow_hours = sma_slow_hours

    @staticmethod
    def _get_sma(series, periods):
        return series.rolling(periods).mean()

    @staticmethod
    def _get_signal(fast, slow):
        print(f"Fast {fast[-1]} / Slow: {slow[-1]}")
        return fast[-1] > slow[-1]

    def _get_bars(self, symbol):
        print(f"Bar Received: {symbol}")

        now = datetime.now()

        sma_slow_days = math.ceil(self._sma_slow_hours / 24)
        delta = timedelta(days=sma_slow_days + 1)
        start = now - delta

        bars = alpaca_rest_client.get_crypto_bars(
            symbol,
            TimeFrame.Hour,
            exchanges=["CBSE"],
            start=start.strftime("%Y-%m-%d"),
        ).df

        bars[f"sma_fast"] = self._get_sma(bars.close, self._sma_fast_hours)
        bars[f"sma_slow"] = self._get_sma(bars.close, self._sma_slow_hours)
        return bars

    async def process_bar(self, bar):
        symbol = bar.symbol.replace("/", "")

        bars = self._get_bars(symbol=symbol)
        signal = self._get_signal(bars.sma_fast, bars.sma_slow)
        return signal

