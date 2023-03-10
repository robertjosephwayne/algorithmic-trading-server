import math
from connectors.alpaca.rest.client import alpaca_rest_client
from strategies.moving_average_crossover import MovingAverageCrossoverStrategy

moving_average_crossover = MovingAverageCrossoverStrategy(
    sma_fast_hours=79, sma_slow_hours=143
)


class Bot:
    def __init__(self, max_allocation):
        super().__init__()
        self._max_allocation = max_allocation

    @staticmethod
    def _get_position(symbol):
        positions = alpaca_rest_client.list_positions()

        for p in positions:
            if p.symbol == symbol:
                return float(p.qty)
        return 0

    @staticmethod
    def _get_non_marginable_buying_power():
        account = alpaca_rest_client.get_account()
        return float(account.non_marginable_buying_power)

    def _get_max_position(self):
        non_marginable_buying_power = self._get_non_marginable_buying_power()
        return math.floor(min(self._max_allocation, non_marginable_buying_power))

    async def process_bar(self, bar):
        signal = await moving_average_crossover.process_bar(bar)
        symbol = bar.symbol.replace("/", "")

        position = self._get_position(symbol=symbol)
        max_position = self._get_max_position()

        print(f"Current position: {position}")
        print(f"Max position: {max_position}")
        print(f"Signal: {signal}")

        if position == 0 and signal:
            print(
                f"Symbol: {symbol} / Side: BUY / Notional Amount: {max_position}"
            )
            alpaca_rest_client.submit_order(
                symbol=symbol,
                notional=max_position,
                side="buy",
                time_in_force="gtc",
            )
        elif position > 0 and not signal:
            print(f"Symbol: {symbol} / Side: SELL / Quantity: {position}")
            alpaca_rest_client.submit_order(
                symbol=symbol, qty=position, side="sell", time_in_force="gtc"
            )
