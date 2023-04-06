from connectors.tradier.rest.client import tradier_rest_client


class Market:
    @staticmethod
    def get_quotes(symbols: str):
        quotes = tradier_rest_client.get_quotes(symbols=symbols)
        return quotes

    @staticmethod
    def get_option_chains(symbol: str, expiration: str, greeks: bool = False):
        option_chains = tradier_rest_client.get_option_chains(symbol=symbol, expiration=expiration, greeks=greeks)
        return option_chains

    @staticmethod
    def get_option_strikes(symbol: str, expiration: str):
        option_strikes = tradier_rest_client.get_option_strikes(symbol=symbol, expiration=expiration)
        return option_strikes

    @staticmethod
    def get_option_expirations(symbol: str):
        option_expirations = tradier_rest_client.get_option_expirations(symbol=symbol)
        return option_expirations

    @staticmethod
    def lookup_option_symbols(underlying: str):
        option_symbols = tradier_rest_client.lookup_option_symbols(underlying=underlying)
        return option_symbols

    @staticmethod
    def get_historical_quotes(symbol: str, start: str, end: str, interval: str = "daily"):
        historical_quotes = tradier_rest_client.get_historical_quotes(symbol=symbol, start=start, end=end,
                                                                      interval=interval)
        return historical_quotes

    @staticmethod
    def get_time_and_sales(symbol: str, interval: str, start: str, end: str):
        time_and_sales = tradier_rest_client.get_time_and_sales(symbol=symbol, interval=interval, start=start, end=end)
        return time_and_sales

    @staticmethod
    def get_etb_securities():
        etb_securities = tradier_rest_client.get_etb_list()
        return etb_securities

    @staticmethod
    def get_clock():
        clock = tradier_rest_client.get_clock()
        return clock

    @staticmethod
    def get_calendar(month: str, year: str):
        calendar = tradier_rest_client.get_calendar(month=month, year=year)
        return calendar

    @staticmethod
    def search_companies(query: str):
        companies = tradier_rest_client.search_companies(query=query)
        return companies

    @staticmethod
    def lookup_symbol(query: str):
        symbol = tradier_rest_client.lookup_symbol(query=query)
        return symbol
