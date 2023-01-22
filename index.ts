import dotenv from 'dotenv';
dotenv.config();

import express, { Express, Request, Response } from 'express';
import { Server } from 'socket.io';
import http from 'http';
import { websocketClient } from '@polygon.io/client-js';
import apiRouter from './src/routes/api';

const POLYGON_API_KEY = process.env.POLYGON_API_KEY || '';
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

server.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});

const cryptoWS = websocketClient(POLYGON_API_KEY).crypto();

cryptoWS.onmessage = ({ data }) => {
    const [result] = JSON.parse(data);
    if (result.message === 'authenticated') {
        cryptoWS.send(JSON.stringify({ action: 'subscribe', params: 'XT.X:BTC-USD' }));
    }
    io.emit('bar', result);
};

app.use('/api', apiRouter);
