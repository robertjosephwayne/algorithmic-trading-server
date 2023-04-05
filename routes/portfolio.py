from fastapi import APIRouter
from models.portfolio import Portfolio

router = APIRouter(
    prefix="/api/portfolio",
    tags=["portfolio"]
)


@router.get("/positions")
async def get_positions():
    positions = await Portfolio.get_positions()
    return positions


@router.get("/activities")
async def get_activities():
    activities = await Portfolio.get_activities()
    return activities


@router.get("/deposits")
async def get_deposits():
    deposits = await Portfolio.get_deposits()
    return deposits


@router.get("/orders")
async def get_orders():
    orders = await Portfolio.get_orders()
    return orders


@router.get("/history")
async def get_history():
    history = await Portfolio.get_history()
    return history


@router.get("/metrics")
async def get_metrics():
    metrics = await Portfolio.get_metrics()
    return metrics