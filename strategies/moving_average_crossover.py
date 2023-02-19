from datetime import datetime, timedelta
from alpaca_trade_api.rest import TimeFrame
from connectors.alpaca.rest.client import alpaca_rest_client


class MovingAverageCrossoverStrategy:
    def __init__(self, sma_fast, sma_slow, usd_per_trade):
        super().__init__()
        self._sma_fast = sma_fast
        self._sma_slow = sma_slow
        self._usd_per_trade = usd_per_trade

    @staticmethod
    def _get_position(symbol):
        positions = alpaca_rest_client.list_positions()
        for p in positions:
            if p.symbol == symbol:
                return float(p.qty)
        return 0

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
        delta = timedelta(days=2)
        start = now - delta

        bars = alpaca_rest_client.get_crypto_bars(symbol, TimeFrame.Minute, exchanges=["CBSE"], start=start.strftime("%Y-%m-%d")).df

        bars[f"sma_fast"] = self._get_sma(bars.close, self._sma_fast)
        bars[f"sma_slow"] = self._get_sma(bars.close, self._sma_slow)
        return bars

    async def process_bar(self, bar):
        symbol = bar.symbol.replace("/", "")

        bars = self._get_bars(symbol=symbol)

        position = self._get_position(symbol=symbol)
        should_buy = self._get_signal(bars.sma_fast, bars.sma_slow)

        if position == 0 and should_buy == True:
            print(f"Symbol: {symbol} / Side: BUY / Notional Amount: {self._usd_per_trade}")
            alpaca_rest_client.submit_order(
                symbol=symbol, notional=self._usd_per_trade, side="buy", time_in_force="gtc"
            )
        elif position > 0 and should_buy == False:
            print(f"Symbol: {symbol} / Side: SELL / Quantity: {position}")
            alpaca_rest_client.submit_order(symbol=symbol, qty=position, side="sell", time_in_force="gtc")