import express from 'express';
import { getCryptoBars, getLatestCryptoTrades } from '../controllers/alpaca';
const router = express.Router();
import { getSnapshotAllTickers, getTickers } from '../controllers/polygon';

router.get('/tickers/crypto', getTickers);

router.get('/snapshot/markets/crypto/tickers', getSnapshotAllTickers);

router.get('/trades/latest', getLatestCryptoTrades);

router.get('/crypto/bars/:symbol', getCryptoBars);

export = router;
