from connectors.tradier.rest.client import tradier_rest_client


class Account:
    @staticmethod
    async def get_summary():
        balances = tradier_rest_client.get_balances()

        summary = {
            "cash": balances.total_cash,
            "long_market_value": balances.long_market_value,
            "short_market_value": balances.short_market_value,
            "market_value": balances.market_value,
            "equity": balances.total_equity,
            "stock_buying_power": balances.margin.stock_buying_power,
            "option_buying_power": balances.margin.option_buying_power,
        }

        return summary

    @staticmethod
    async def get_positions():
        positions = tradier_rest_client.get_positions()
        return positions

    @staticmethod
    async def get_history():
        history = tradier_rest_client.get_history()
        return history

    @staticmethod
    async def get_gain_loss():
        gain_loss = tradier_rest_client.get_gain_loss()
        return gain_loss

    @staticmethod
    async def get_orders():
        orders = tradier_rest_client.get_orders()
        return orders

    @staticmethod
    async def get_order(order_id: str):
        order = tradier_rest_client.get_order(order_id)
        return order
