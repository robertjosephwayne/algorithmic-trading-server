from config import config
from tradier_python import TradierAPI

trading_mode = "PAPER"
if config["TRADIER"]["ENABLE_LIVE_TRADING"]:
    trading_mode = "LIVE"

account_number = config["TRADIER"][trading_mode]["ACCOUNT_NUMBER"]
access_token = config["TRADIER"][trading_mode]["ACCESS_TOKEN"]

tradier_rest_client = TradierAPI(token=access_token, default_account_id=account_number)
