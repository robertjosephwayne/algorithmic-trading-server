from connectors.alpaca.websocket.client import AlpacaWebSocketClient
from config import config
from bot import Bot
from fastapi import FastAPI
from fastapi_socketio import SocketManager
from routes import account, market, portfolio, trades
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk

sentry_sdk.init(dsn=config["SENTRY_DSN"], traces_sample_rate=1.0)

app = FastAPI()
app.include_router(account.router)
app.include_router(market.router)
app.include_router(portfolio.router)
app.include_router(trades.router)

origins = [config["CLIENT_URL"]]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_manager = SocketManager(app=app, mount_location="/")
bot = Bot(max_allocation=10000)

alpaca = AlpacaWebSocketClient()
alpaca.subscribe_bars("crypto", ["BTC/USD"], bot.process_bar)
alpaca.connect()
