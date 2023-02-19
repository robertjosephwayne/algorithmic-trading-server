from connectors.alpaca.websocket.client import AlpacaWebSocketClient
from config import config
from bot import process_bar
from fastapi import FastAPI
from fastapi_socketio import SocketManager
from routes import crypto
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(crypto.router)

origins = [config["CLIENT_URL"]]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_manager = SocketManager(app=app, mount_location="/")

alpaca = AlpacaWebSocketClient()
alpaca.subscribe_bars(["BTC/USD"], process_bar)
alpaca.connect()
