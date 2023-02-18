from fastapi import APIRouter
import urllib.parse
from alpaca_trade_api.rest import TimeFrame, URL, REST, TimeFrameUnit
from config import config
from pyrfc3339 import parse

router = APIRouter(
    prefix="/api/crypto"
)

base_url = URL("https://paper-api.alpaca.markets")
data_feed = "sip"
rest = REST(key_id=config["ALPACA"]["API_KEY"], secret_key=config["ALPACA"]["SECRET_KEY"], base_url=base_url)
supported_tickers = ["BTCUSD", "ETHUSD", "LTCUSD", "BCHUSD"]


@router.get("/bars/{symbol}")
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

    bars = rest.get_crypto_bars(symbol, alpaca_timeframe, start, limit=60, exchanges=['CBSE'])

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


@router.get("/bars/latest")
async def get_latest_crypto_bars():
    result = rest.get_latest_crypto_bars(supported_tickers, "CBSE")

    response = {}

    for ticker in supported_tickers:
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


@router.get("/trades/latest")
async def get_latest_crypto_trades():
    result = rest.get_latest_crypto_trades(supported_tickers, "CBSE")

    response = {}

    for ticker in supported_tickers:
        trade = result[ticker]
        response[ticker] = {
            "price": trade.price,
            "timestamp": trade.timestamp,
            "exchange": trade.x
        }

    return response


@router.get("/account")
async def get_account():
    result = rest.get_account()

    response = {
        "cash": result.cash,
        "position_market_value": result.position_market_value,
        "equity": result.equity,
        "buying_power": result.buying_power
    }

    return response


@router.get("/positions")
async def get_positions():
    result = rest.list_positions()

    response = []

    for asset in result:
        response.append({
            "symbol": asset.symbol,
            "quantity": asset.qty,
            "side": asset.side,
            "exchange": asset.exchange,
            "cost_basis": asset.cost_basis,
            "market_value": asset.market_value,
        })

    return response


@router.get("/activities")
async def get_activities():
    result = rest.get_activities()

    response = []

    for activity in result:
        response.append({
            "activity_type": activity.activity_type,
            "cumulative_quantity": activity.cum_qty,
            "order_status": activity.order_status,
            "price": activity.price,
            "quantity": activity.qty,
            "side": activity.side,
            "symbol": activity.symbol,
            "transaction_time": activity.transaction_time,
            "type": activity.type
        })

    return response


@router.get("/portfolio-history")
async def get_portfolio_history(timeframe, start):
    start = urllib.parse.unquote(start)
    start = parse(start).strftime("%Y-%m-%d")

    alpaca_timeframe = None
    match timeframe:
        case '1M':
            alpaca_timeframe = "1Min"
        case '5M':
            alpaca_timeframe = "5Min"
        case '15M':
            alpaca_timeframe = "15Min"
        case '1H':
            alpaca_timeframe = timeframe
        case '1D':
            alpaca_timeframe = timeframe

    result = rest.get_portfolio_history(date_start=start, timeframe=alpaca_timeframe)
    response = []

    for i in range(len(result.equity)):
        response.append({
            "timestamp": result.timestamp[i] * 1000,
            "equity": result.equity[i]
        })

    return response
