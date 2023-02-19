from config import config
from alpaca_trade_api.rest import URL, REST

base_url = URL("https://paper-api.alpaca.markets")
api_key = config["ALPACA"]["PAPER"]["API_KEY"]
secret_key = config["ALPACA"]["PAPER"]["SECRET_KEY"]
data_feed = "sip"

if config["ALPACA"]["ENABLE_LIVE_TRADING"]:
    base_url = URL("https://api.alpaca.markets")
    api_key = config["ALPACA"]["LIVE"]["API_KEY"]
    secret_key = config["ALPACA"]["LIVE"]["SECRET_KEY"]

alpaca_rest_client = REST(key_id=api_key, secret_key=secret_key, base_url=base_url,)
