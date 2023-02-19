import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "ALPACA": {
        "LIVE": {
            "API_KEY": os.environ.get("ALPACA_LIVE_API_KEY"),
            "SECRET_KEY": os.environ.get("ALPACA_LIVE_API_SECRET"),
        },
        "BACKTEST": {
            "API_KEY": os.environ.get("ALPACA_BACKTEST_API_KEY"),
            "SECRET_KEY": os.environ.get("ALPACA_BACKTEST_API_SECRET"),
        }
    },
    "CLIENT_URL": os.environ.get("CLIENT_URL"),
}
