from fastapi import APIRouter
from models.account import Account

router = APIRouter(
    prefix="/api/account",
    tags=["account"]
)


@router.get("/summary")
async def get_summary():
    summary = await Account.get_summary()
    return summary


@router.get("/positions")
async def get_positions():
    positions = await Account.get_positions()
    return positions


@router.get("/history")
async def get_history():
    history = await Account.get_history()
    return history


@router.get("/gain-loss")
async def get_gain_loss():
    gain_loss = await Account.get_gain_loss()
    return gain_loss


@router.get("/orders")
async def get_orders():
    orders = await Account.get_orders()
    return orders


@router.get("/order/{order_id}")
async def get_order(order_id: str):
    order = await Account.get_order(order_id)
    return order