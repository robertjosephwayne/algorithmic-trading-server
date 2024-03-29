import math
from connectors.alpaca.rest.client import alpaca_rest_client
from strategies.moving_average_crossover import MovingAverageCrossoverStrategy
from datetime import datetime
from rfc3339 import rfc3339

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
        await self.process_crypto_bar(bar)
        await self.process_stock_bar(bar)

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

        clock = alpaca_rest_client.get_clock()
        if not clock.is_open:
            print("Market is closed. Skipping...")
            return

        positions = alpaca_rest_client.list_positions()
        activities = alpaca_rest_client.get_activities(activity_types="FILL", direction="desc")

        trading_start = datetime(2023, 3, 1, 0, 0)

        etf_historical_prices = {}
        etf_tickers = ['SPY', 'QQQ']
        for etf_ticker in etf_tickers:
            prices = alpaca_rest_client.get_bars(etf_ticker, start=rfc3339(trading_start), timeframe="1Min")
            etf_historical_prices[etf_ticker] = prices

        etf_latest_price = {}
        for etf_ticker in etf_tickers:
            latest_price = alpaca_rest_client.get_latest_bar(etf_ticker)
            etf_latest_price[etf_ticker] = latest_price.c

        for position in positions:
            if position.side == "short":
                stop_percent = 7

                position_current_price = float(position.current_price)
                position_average_entry_price = float(position.avg_entry_price)

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

                if position.exchange == 'NASDAQ':
                    etf = 'QQQ'
                elif position.exchange == 'NYSE':
                    etf = 'SPY'

                etf_average_entry_price = None
                transaction_time = last_short_sell_activity.transaction_time.strftime('%Y-%m-%d %H:%MZ')
                for bar in etf_historical_prices[etf]:
                    bar_time_utc = bar.t.tz_convert(tz='UTC').strftime('%Y-%m-%d %H:%MZ')

                    if bar_time_utc == transaction_time:
                        etf_average_entry_price = float(bar.c)
                        break

                if not etf_average_entry_price:
                    print(
                        f'Unable to find ETF entry price for {etf} at {transaction_time}. This is related to {position.symbol}.')
                    return

                ratio_average_entry = (position_average_entry_price / etf_average_entry_price) * 100
                ratio_today = (position_current_price / etf_latest_price[etf] * 100)
                ratio_percent_change = (ratio_today / ratio_average_entry - 1) * 100

                print(f'Ratio change for {position.symbol}: {ratio_percent_change}')

                # Submit stop loss orders
                should_place_stop_loss_order = False

                # If profit has already been taken, exit position when relative change is zero or greater
                if already_placed_take_profit_order and ratio_percent_change >= 0:
                    should_place_stop_loss_order = True

                if ratio_percent_change >= stop_percent:
                    should_place_stop_loss_order = True

                if should_place_stop_loss_order:
                    print(f"Submitting stop loss order for {position.symbol}")
                    exit_quantity = -float(position.qty)
                    exit_notional_value = exit_quantity * position_current_price

                    alpaca_rest_client.submit_order(
                        symbol=position.symbol,
                        qty=-float(position.qty),
                        side="buy",
                        type="market",
                        time_in_force="day"
                    )

                    print(f"Submitting sell order for {etf}. Notional value: {exit_notional_value}")
                    alpaca_rest_client.submit_order(
                        symbol=etf,
                        notional=exit_notional_value,
                        side="sell",
                        type="market",
                        time_in_force="day"
                    )

                    continue

                # Submit take profit orders

                open_orders = alpaca_rest_client.list_orders(status="open", symbols=[position.symbol])

                take_profit_ratio_percent_change = stop_percent * 1.1

                should_place_take_profit_order = False
                if ratio_percent_change <= -take_profit_ratio_percent_change and not already_placed_take_profit_order:
                    should_place_take_profit_order = True

                if len(open_orders):
                    print(f"Open orders exist. Not placing take profit order for symbol: {position.symbol}.")
                    should_place_take_profit_order = False

                # If current price has reached 1.1R, exit 50% of position
                if should_place_take_profit_order:
                    print(f"Submitting take profit order for {position.symbol}")
                    exit_quantity = -float(position.qty) * .5
                    exit_quantity = round(exit_quantity, 2)
                    exit_notional_value = exit_quantity * position_current_price

                    alpaca_rest_client.submit_order(
                        symbol=position.symbol,
                        qty=exit_quantity,
                        side="buy",
                        type="market",
                        time_in_force="day"
                    )

                    print(f"Submitting sell order for {etf}. Notional value: {exit_notional_value}")
                    alpaca_rest_client.submit_order(
                        symbol=etf,
                        notional=exit_notional_value,
                        side="sell",
                        type="market",
                        time_in_force="day"
                    )