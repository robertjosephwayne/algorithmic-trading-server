import dotenv from 'dotenv';
dotenv.config();

import express, { Express, Request, Response } from 'express';
import { Server } from 'socket.io';
import http from 'http';
import cors from 'cors';
import apiRouter from './src/routes/api';
import Alpaca from '@alpacahq/alpaca-trade-api';
import { SUPPORTED_TICKERS } from './constants';

const ALPACA_API_KEY = process.env.ALPACA_API_KEY || '';
const ALPACA_API_SECRET = process.env.ALPACA_API_SECRET || '';
const PORT = process.env.PORT || 8000;
const CLIENT_URL = process.env.CLIENT_URL || 'http://localhost:3000';

const app: Express = express();
const server = http.createServer(app);

const corsOptions = {
    origin: CLIENT_URL,
};

const io = new Server(server, {
    cors: corsOptions,
});

io.on('connection', (socket) => {
    console.log('A new connection has been established.');
});

server.listen(PORT, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${PORT}`);
});

app.use('/api', cors(corsOptions), apiRouter);

const alpaca = new Alpaca({
    keyId: ALPACA_API_KEY,
    secretKey: ALPACA_API_SECRET,
    feed: 'sip',
    paper: true,
});

const socket = alpaca.crypto_stream_v2;

socket.onConnect(function () {
    socket.subscribeForTrades(SUPPORTED_TICKERS);
});

socket.onCryptoTrade(function (trade) {
    if (trade.Exchange === 'CBSE') {
        io.emit('bar', trade);
    }
});

socket.connect();
