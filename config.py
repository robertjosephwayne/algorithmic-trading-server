import os
from dotenv import load_dotenv
load_dotenv()

config = {
    "ALPACA": {
        "API_KEY": os.environ.get('ALPACA_API_KEY'),
        "SECRET_KEY": os.environ.get('ALPACA_API_SECRET'),
    },
    "CLIENT_URL": os.environ.get('CLIENT_URL')
}
