from fastapi import APIRouter
import urllib.parse
from alpaca_trade_api.rest import TimeFrame, TimeFrameUnit
from pyrfc3339 import parse
from connectors.alpaca.rest.client import alpaca_rest_client

router = APIRouter(
    prefix="/api/crypto"
)

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


@router.get("/bars/latest")
async def get_latest_crypto_bars():
    result = alpaca_rest_client.get_latest_crypto_bars(supported_tickers, "CBSE")

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
    result = alpaca_rest_client.get_latest_crypto_trades(supported_tickers, "CBSE")

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
    result = alpaca_rest_client.get_account()

    response = {
        "cash": result.cash,
        "position_market_value": result.position_market_value,
        "equity": result.equity,
        "buying_power": result.buying_power
    }

    return response


@router.get("/positions")
async def get_positions():
    result = alpaca_rest_client.list_positions()

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
    result = alpaca_rest_client.get_activities()

    response = []

    for activity in result:
        if activity.activity_type == "FILL":
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


@router.get("/orders")
async def get_orders():
    result = alpaca_rest_client.list_orders()

    response = []

    for order in result:
        response.append({
            "symbol": order.symbol,
            "quantity": order.qty,
            "filled_quantity": order.filled_qty,
            "side": order.side,
            "type": order.type,
            "time_in_force": order.time_in_force,
            "limit_price": order.limit_price,
            "stop_price": order.stop_price,
            "notional": order.notional,
            "trail_percent": order.trail_percent,
            "trail_price": order.trail_price
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

    result = alpaca_rest_client.get_portfolio_history(date_start=start, timeframe=alpaca_timeframe)
    response = []

    for i in range(len(result.equity)):
        response.append({
            "timestamp": result.timestamp[i] * 1000,
            "equity": result.equity[i]
        })

    return response


@router.post("/stop")
async def place_stop_orders():
    return

    positions = alpaca_rest_client.list_positions()

    for position in positions:
        if position.side == "short":
            print(position.symbol)

            alpaca_rest_client.submit_order(
                symbol=position.symbol,
                qty=-int(position.qty),
                side="buy",
                type="trailing_stop",
                time_in_force="gtc",
                trail_percent="10"
            )