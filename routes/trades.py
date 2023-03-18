from fastapi import APIRouter
from models.trade import Trade

router = APIRouter(
    prefix="/api/trades",
    tags=["trades"]
)


@router.get("/history")
async def get_history():
    history = await Trade.get_history()
    return history
