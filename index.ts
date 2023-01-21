import express, { Express, Request, Response } from 'express';
import { Server } from 'socket.io';
import http from 'http';
import dotenv from 'dotenv';

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
    console.log('a user connected');
    socket.on('ping', () => {
        console.log('ping');
        socket.emit('pong');
    });
});

app.get('/', (req: Request, res: Response) => {
    res.send('Express + TypeScript Server');
});

server.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
