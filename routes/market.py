from fastapi import APIRouter
from models.market import Market

router = APIRouter(
    prefix="/api/market",
    tags=["market"]
)


@router.get("/quotes")
def get_quotes(symbols: str):
    quotes = Market.get_quotes(symbols=symbols)
    return quotes


@router.get("/option-chains")
def get_option_chains(symbol: str, expiration: str, greeks: bool = False):
    option_chains = Market.get_option_chains(symbol=symbol, expiration=expiration, greeks=greeks)
    return option_chains


@router.get("/option-strikes")
def get_option_strikes(symbol: str, expiration: str):
    option_strikes = Market.get_option_strikes(symbol=symbol, expiration=expiration)
    return option_strikes


@router.get("/option-expirations")
def get_option_expirations(symbol: str):
    option_expirations = Market.get_option_expirations(symbol=symbol)
    return option_expirations


@router.get("/option-symbols")
def lookup_option_symbols(underlying: str):
    option_symbols = Market.lookup_option_symbols(underlying=underlying)
    return option_symbols


@router.get("/historical-quotes")
def get_historical_quotes(symbol: str, start: str, end: str, interval: str = "daily"):
    historical_quotes = Market.get_historical_quotes(symbol=symbol, start=start, end=end, interval=interval)
    return historical_quotes


@router.get("/time-and-sales")
def get_time_and_sales(symbol: str, interval: str, start: str, end: str):
    time_and_sales = Market.get_time_and_sales(symbol=symbol, interval=interval, start=start, end=end)
    return time_and_sales


@router.get("/etb-securities")
def get_etb_securities():
    etb_securities = Market.get_etb_securities()
    return etb_securities


@router.get("/clock")
def get_clock():
    clock = Market.get_clock()
    return clock


@router.get("/calendar")
def get_calendar(month: str, year: str):
    calendar = Market.get_calendar(month=month, year=year)
    return calendar


@router.get("/companies")
def search_companies(query: str):
    companies = Market.search_companies(query=query)
    return companies


@router.get("/symbol")
def lookup_symbol(query: str):
    symbol = Market.lookup_symbol(query=query)
    return symbol
