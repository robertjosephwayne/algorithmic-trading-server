from config import config
from alpaca_trade_api.rest import URL, REST

trading_mode = "PAPER"
if config["ALPACA"]["ENABLE_LIVE_TRADING"]:
    trading_mode = "LIVE"

base_url = URL(config["ALPACA"][trading_mode]["ENDPOINT"])
api_key = config["ALPACA"][trading_mode]["API_KEY"]
secret_key = config["ALPACA"][trading_mode]["SECRET_KEY"]
data_feed = "sip"

alpaca_rest_client = REST(key_id=api_key, secret_key=secret_key, base_url=base_url,)
