from fastapi import APIRouter
import urllib.parse
from alpaca_trade_api.rest import TimeFrame, TimeFrameUnit
from connectors.alpaca.rest.client import alpaca_rest_client

router = APIRouter(
    prefix="/api/market"
)

supported_crypto_tickers = ["BTCUSD", "ETHUSD", "LTCUSD", "BCHUSD"]


@router.get("/crypto/bars/{symbol}")
async def get_crypto_bars(symbol, timeframe, start):
    start = urllib.parse.unquote(start)

    alpaca_timeframe = None
    match timeframe:
        case 'minute':
            alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Minute)
        case 'hour':
            alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Hour)
        case 'day':
            alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Day)
        case 'week':
            alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Week)
        case 'month':
            alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Month)

    bars = alpaca_rest_client.get_crypto_bars(symbol, alpaca_timeframe, start, limit=60, exchanges=['CBSE'])

    response = list()

    for bar in bars:
        response.append({
            "symbol": symbol,
            "timestamp": bar.t,
            "high": bar.h,
            "low": bar.l,
            "open": bar.o,
            "close": bar.c,
            "exchange": bar.x
        })

    return response


@router.get("/crypto/bars/latest")
async def get_latest_crypto_bars():
    result = alpaca_rest_client.get_latest_crypto_bars(supported_crypto_tickers, "CBSE")

    response = {}

    for ticker in supported_crypto_tickers:
        bar = result[ticker]
        response[ticker] = {
            "high": bar.h,
            "low": bar.l,
            "open": bar.o,
            "close": bar.c,
            "timestamp": bar.t,
            "volume": bar.v,
            "weighted_volume": bar.vw,
            "exchange": bar.x
        }

    return response


@router.get("/crypto/trades/latest")
async def get_latest_crypto_trades():
    result = alpaca_rest_client.get_latest_crypto_trades(supported_crypto_tickers, "CBSE")

    response = {}

    for ticker in supported_crypto_tickers:
        trade = result[ticker]
        response[ticker] = {
            "price": trade.price,
            "timestamp": trade.timestamp,
            "exchange": trade.x
        }

    return response
