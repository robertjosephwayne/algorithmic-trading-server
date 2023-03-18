from fastapi import APIRouter
from models.market import Market
import urllib.parse

router = APIRouter(
    prefix="/api/market"
)


@router.get("/crypto/bars/latest")
async def get_latest_crypto_bars():
    latest_bars = await Market.get_crypto_latest_bars()
    return latest_bars


@router.get("/crypto/bars/{symbol}")
async def get_crypto_bars(symbol, timeframe, start):
    start = urllib.parse.unquote(start)
    bars = await Market.get_crypto_bars(symbol=symbol, timeframe=timeframe, start=start)
    return bars


@router.get("/crypto/trades/latest")
async def get_latest_crypto_trades():
    trades = await Market.get_crypto_latest_trades()
    return trades
