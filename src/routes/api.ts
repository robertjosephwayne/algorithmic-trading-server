import express from 'express';
const router = express.Router();
import { getSnapshotAllTickers, getTickers } from '../controllers/crypto';

router.get('/tickers/crypto', getTickers);

router.get('/snapshot/markets/crypto/tickers', getSnapshotAllTickers);

export = router;
