import { Request, Response } from 'express';
import Alpaca from '@alpacahq/alpaca-trade-api';
import { SUPPORTED_TICKERS } from '../../constants';

const ALPACA_API_KEY = process.env.ALPACA_API_KEY || '';
const ALPACA_API_SECRET = process.env.ALPACA_API_SECRET || '';
const alpaca = new Alpaca({
    keyId: ALPACA_API_KEY,
    secretKey: ALPACA_API_SECRET,
    paper: true,
});

const getLatestCryptoTrades = async (req: Request, res: Response) => {
    const result = await alpaca.getLatestCryptoTrades(SUPPORTED_TICKERS, { exchange: 'CBSE' });

    const response: any = {};

    for (const ticker of SUPPORTED_TICKERS) {
        const lastTrade = result.get(ticker);
        response[ticker] = lastTrade;
    }

    return res.send(response);
};

const getCryptoBars = async (req: Request, res: Response) => {
    const symbol = req.params.symbol;
    const timeframe = req.query.timeframe;
    let start = '2023-01-01';
    if (typeof req.query.start === 'string') {
        start = decodeURIComponent(req.query.start);
    }

    let interval = 1;
    if (typeof req.query.interval === 'string') {
        interval = parseInt(req.query.interval);
    }

    let alpacaTimeframe;
    switch (timeframe) {
        case 'minute':
            alpacaTimeframe = alpaca.newTimeframe(interval, alpaca.timeframeUnit.MIN);
            break;
        case 'hour':
            alpacaTimeframe = alpaca.newTimeframe(interval, alpaca.timeframeUnit.HOUR);
            break;
        case 'day':
            alpacaTimeframe = alpaca.newTimeframe(interval, alpaca.timeframeUnit.DAY);
            break;
        case 'week':
            alpacaTimeframe = alpaca.newTimeframe(interval, alpaca.timeframeUnit.WEEK);
            break;
        case 'month':
            alpacaTimeframe = alpaca.newTimeframe(interval, alpaca.timeframeUnit.MONTH);
            break;
        default:
            return res.sendStatus(400);
    }

    const result = await alpaca.getCryptoBars(symbol, {
        timeframe: alpacaTimeframe,
        start,
        exchanges: 'CBSE',
    });

    const bars = [];

    for await (const bar of result) {
        bars.push(bar);
    }

    return res.send(bars);
};

export { getCryptoBars, getLatestCryptoTrades };
