from connectors.alpaca.rest.client import alpaca_rest_client
from alpaca_trade_api.rest import TimeFrame, TimeFrameUnit

supported_crypto_tickers = ["BTCUSD", "ETHUSD", "LTCUSD", "BCHUSD"]


class Market:
    @staticmethod
    async def get_crypto_bars(symbol, timeframe, start):
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

        formatted_bars = list()

        for bar in bars:
            formatted_bars.append({
                "symbol": symbol,
                "timestamp": bar.t,
                "high": bar.h,
                "low": bar.l,
                "open": bar.o,
                "close": bar.c,
                "exchange": bar.x
            })

        return formatted_bars

    @staticmethod
    async def get_crypto_latest_bars():
        response = alpaca_rest_client.get_latest_crypto_bars(supported_crypto_tickers, "CBSE")

        bars_by_ticker = {}

        for ticker in supported_crypto_tickers:
            bar = response[ticker]
            bars_by_ticker[ticker] = {
                "high": bar.h,
                "low": bar.l,
                "open": bar.o,
                "close": bar.c,
                "timestamp": bar.t,
                "volume": bar.v,
                "weighted_volume": bar.vw,
                "exchange": bar.x
            }

        return bars_by_ticker

    @staticmethod
    async def get_crypto_latest_trades():
        response = alpaca_rest_client.get_latest_crypto_trades(supported_crypto_tickers, "CBSE")

        trades_by_ticker = {}

        for ticker in supported_crypto_tickers:
            trade = response[ticker]
            trades_by_ticker[ticker] = {
                "price": trade.price,
                "timestamp": trade.timestamp,
                "exchange": trade.x
            }

        return trades_by_ticker
