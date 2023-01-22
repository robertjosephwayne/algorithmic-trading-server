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

export { getTickers };
