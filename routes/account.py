from fastapi import APIRouter
from models.account import Account

router = APIRouter(
    prefix="/api/account"
)


@router.get("/summary")
async def get_summary():
    summary = await Account.get_summary()
    return summary
