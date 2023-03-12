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

    async def process_crypto_bar(self, bar):
        print("Processing crypto bar...")

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

    async def process_stock_bar(self, bar):
        print("Processing stock bar...")

        positions = alpaca_rest_client.list_positions()
        activities = alpaca_rest_client.get_activities(activity_types="FILL", direction="desc")

        for position in positions:
            if position.side == "short":
                # Submit stop loss orders

                stop_percent = 10

                stop_price = float(position.avg_entry_price) * (1 + stop_percent / 100)
                current_price = float(position.current_price)

                if current_price >= stop_price:
                    print(f"Submitting stop loss order for {position.symbol}")

                    alpaca_rest_client.submit_order(
                        symbol=position.symbol,
                        qty=-int(position.qty),
                        side="buy",
                        type="market",
                        time_in_force="day"
                    )

                # Submit take profit orders

                short_sell_activities = filter(lambda activity:
                                        activity.symbol == position.symbol
                                        and activity.side == "sell_short",
                                        activities)
                short_sell_activities = list(short_sell_activities)

                buy_activities = filter(lambda activity:
                                        activity.symbol == position.symbol
                                        and activity.side == "buy",
                                        activities)
                buy_activities = list(buy_activities)

                last_short_sell_activity = short_sell_activities[0]
                last_buy_activity = None
                if len(buy_activities):
                    last_buy_activity = buy_activities[0]

                already_placed_take_profit_order = False

                if last_buy_activity and last_buy_activity.transaction_time > last_short_sell_activity.transaction_time:
                    already_placed_take_profit_order = True

                if already_placed_take_profit_order:
                    return

                # If current price has reached 1.1R, exit 91% of position
                elif current_price <= float(position.avg_entry_price) * (1 - (stop_percent * 1.1) / 100):
                    print(f"Submitting take profit order for {position.symbol}")
                    exit_quantity = -int(position.qty) * .91
                    exit_quantity = round(exit_quantity, 2)

                    alpaca_rest_client.submit_order(
                        symbol=position.symbol,
                        qty=exit_quantity,
                        side="buy",
                        type="market",
                        time_in_force="day"
                    )
