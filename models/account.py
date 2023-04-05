from connectors.alpaca.rest.client import alpaca_rest_client
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
