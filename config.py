import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "ALPACA": {
        "ENABLE_LIVE_TRADING": True,
        "LIVE": {
            "API_KEY": os.environ.get("ALPACA_LIVE_API_KEY"),
            "SECRET_KEY": os.environ.get("ALPACA_LIVE_API_SECRET"),
        },
        "PAPER": {
            "API_KEY": os.environ.get("ALPACA_PAPER_API_KEY"),
            "SECRET_KEY": os.environ.get("ALPACA_PAPER_API_SECRET"),
        }
    },
    "CLIENT_URL": os.environ.get("CLIENT_URL"),
}


