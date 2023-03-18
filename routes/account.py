from fastapi import APIRouter
from connectors.alpaca.rest.client import alpaca_rest_client

router = APIRouter(
    prefix="/api/account"
)


@router.get("/summary")
async def get_account():
    result = alpaca_rest_client.get_account()

    response = {
        "cash": result.cash,
        "position_market_value": result.position_market_value,
        "equity": result.equity,
        "buying_power": result.buying_power
    }

    return response