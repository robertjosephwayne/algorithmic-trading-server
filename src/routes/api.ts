import express from 'express';
const router = express.Router();
import { getTickers } from '../controllers/crypto';

router.get('/tickers/crypto', getTickers);

export = router;
