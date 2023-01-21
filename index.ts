import express, { Express, Request, Response } from 'express';
import { Server } from 'socket.io';
import http from 'http';
import dotenv from 'dotenv';
import Alpaca from '@alpacahq/alpaca-trade-api';

dotenv.config();

const port = process.env.PORT || 8000;
const app: Express = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: process.env.CLIENT_URL || 'http://localhost:3000',
    },
});

io.on('connection', (socket) => {
    console.log('A new connection has been established.');
});

class DataStream {
    alpaca;

    constructor({ apiKey, secretKey, feed, symbol }: any) {
        this.alpaca = new Alpaca({
            keyId: apiKey,
            secretKey,
            feed,
        });

        const socket = this.alpaca.crypto_stream_v2;

        socket.onConnect(function () {
            console.log('Connected');
            socket.subscribeForBars([symbol]);
        });

        socket.onError((err) => {
            console.log(err);
        });

        socket.onCryptoBar((bar) => {
            console.log(bar);
            io.emit('bar', bar);
        });

        socket.onDisconnect(() => {
            console.log('Disconnected');
        });

        socket.connect();
    }
}

const feed = 'iex';
const symbol = 'BTCUSD';

const stream = new DataStream({
    apiKey: process.env.ALPACA_TRADE_API_KEY,
    secretKey: process.env.ALPACA_TRADE_SECRET_KEY,
    feed,
    symbol,
    paper: true,
});

app.get('/', (req: Request, res: Response) => {
    res.send('Express + TypeScript Server');
});

server.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
