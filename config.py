import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "ALPACA": {
        "ENABLE_LIVE_TRADING": os.environ.get("ALPACA_ENABLE_LIVE_TRADING"),
        "LIVE": {
            "API_KEY": os.environ.get("ALPACA_LIVE_API_KEY"),
            "SECRET_KEY": os.environ.get("ALPACA_LIVE_API_SECRET"),
        },
        "PAPER": {
            "API_KEY": os.environ.get("ALPACA_PAPER_API_KEY"),
            "SECRET_KEY": os.environ.get("ALPACA_PAPER_API_SECRET"),
        },
    },
    "CLIENT_URL": os.environ.get("CLIENT_URL"),
}
