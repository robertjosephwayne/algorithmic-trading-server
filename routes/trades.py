from fastapi import APIRouter
from models.trade import Trade

router = APIRouter(
    prefix="/api/trades"
)


@router.get("/history")
async def get_history():
    trade_history = await Trade.get_history()
    return trade_history
