import { Request, Response } from 'express';
import { restClient } from '@polygon.io/client-js';
const polygonRestClient = restClient(process.env.POLYGON_API_KEY);

const getTickers = async (req: Request, res: Response) => {
    const response = await polygonRestClient.reference.tickers({ market: 'crypto' });

    if (response.status === 'OK') {
        const tickersWithDetails = response.results;

        const tickers = tickersWithDetails.map((tickerWithDetails) => {
            return {
                ticker: tickerWithDetails.ticker,
            };
        });
        return res.send(tickers);
    } else {
        return res.sendStatus(500);
    }
};

const getSnapshotAllTickers = async (req: Request, res: Response) => {
    const response = await polygonRestClient.crypto.snapshotAllTickers();

    if (response.status === 'OK' && response.tickers) {
        const tickers = [];

        for (const tickerWithDetails of response?.tickers) {
            if (tickerWithDetails?.lastTrade?.x !== 1) continue;

            let formattedTicker = tickerWithDetails.ticker?.replace('X:', '');
            if (formattedTicker && formattedTicker?.endsWith('USD')) {
                formattedTicker = formattedTicker.slice(0, formattedTicker.length - 3);
                formattedTicker += '-USD';
            }

            tickers.push({
                ...tickerWithDetails,
                ticker: formattedTicker,
            });
        }

        return res.send(tickers);
    } else {
        return res.sendStatus(500);
    }
};

export { getTickers, getSnapshotAllTickers };
