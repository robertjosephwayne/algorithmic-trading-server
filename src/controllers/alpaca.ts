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

export { getLatestCryptoTrades };
