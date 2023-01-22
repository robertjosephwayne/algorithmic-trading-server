import dotenv from 'dotenv';
dotenv.config();

import express, { Express, Request, Response } from 'express';
import { Server } from 'socket.io';
import http from 'http';
import { websocketClient } from '@polygon.io/client-js';
import cors from 'cors';
import apiRouter from './src/routes/api';

const POLYGON_API_KEY = process.env.POLYGON_API_KEY || '';
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

const cryptoWS = websocketClient(POLYGON_API_KEY).crypto();

cryptoWS.onmessage = ({ data }) => {
    const [result] = JSON.parse(data);
    if (result.message === 'authenticated') {
        cryptoWS.send(JSON.stringify({ action: 'subscribe', params: 'XT.X:BTC-USD' }));
    }
    io.emit('bar', result);
};

app.use('/api', cors(corsOptions), apiRouter);
