from connectors.alpaca.rest.client import alpaca_rest_client


class Account:
    @staticmethod
    async def get_summary():
        response = alpaca_rest_client.get_account()

        summary = {
            "cash": response.cash,
            "position_market_value": response.position_market_value,
            "equity": response.equity,
            "buying_power": response.buying_power
        }

        return summary
