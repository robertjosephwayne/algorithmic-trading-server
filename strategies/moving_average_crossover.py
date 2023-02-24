import math
from datetime import datetime, timedelta
from alpaca_trade_api.rest import TimeFrame
from connectors.alpaca.rest.client import alpaca_rest_client


class MovingAverageCrossoverStrategy:
    def __init__(self, sma_fast_hours, sma_slow_hours, max_allocation):
        super().__init__()
        self._sma_fast_hours = sma_fast_hours
        self._sma_slow_hours = sma_slow_hours
        self._max_allocation = max_allocation

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

    @staticmethod
    def _get_non_marginable_buying_power():
        account = alpaca_rest_client.get_account()
        return float(account.non_marginable_buying_power)

    def _get_max_position(self):
        non_marginable_buying_power = self._get_non_marginable_buying_power()
        return math.floor(min(self._max_allocation, non_marginable_buying_power))

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
        position = self._get_position(symbol=symbol)
        should_buy = self._get_signal(bars.sma_fast, bars.sma_slow)

        max_position = self._get_max_position()

        if position < max_position and should_buy == True:
            print(
                f"Symbol: {symbol} / Side: BUY / Notional Amount: {max_position}"
            )
            alpaca_rest_client.submit_order(
                symbol=symbol,
                notional=max_position,
                side="buy",
                time_in_force="gtc",
            )
        elif position > 0 and should_buy == False:
            print(f"Symbol: {symbol} / Side: SELL / Quantity: {position}")
            alpaca_rest_client.submit_order(
                symbol=symbol, qty=position, side="sell", time_in_force="gtc"
            )
