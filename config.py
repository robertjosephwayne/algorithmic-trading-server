import os
from dotenv import load_dotenv
from distutils.util import strtobool

load_dotenv()

config = {
    "ALPACA": {
        "ENABLE_LIVE_TRADING": strtobool(os.environ.get("ALPACA_ENABLE_LIVE_TRADING")),
        "LIVE": {
            "API_KEY": os.environ.get("ALPACA_LIVE_API_KEY"),
            "SECRET_KEY": os.environ.get("ALPACA_LIVE_API_SECRET"),
            "ENDPOINT": "https://api.alpaca.markets"
        },
        "PAPER": {
            "API_KEY": os.environ.get("ALPACA_PAPER_API_KEY"),
            "SECRET_KEY": os.environ.get("ALPACA_PAPER_API_SECRET"),
            "ENDPOINT": "https://paper-api.alpaca.markets"
        },
    },
    "CLIENT_URL": os.environ.get("CLIENT_URL"),
    "SENTRY_DSN": os.environ.get("SENTRY_DSN"),
}
