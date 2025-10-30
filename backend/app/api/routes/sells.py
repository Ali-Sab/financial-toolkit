from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.db.models import User
from app.utils.auth_utils import get_current_user
from app.repositories.sells_repository import sells_repository

router = APIRouter()

@router.get("/accounts/{account_id}/sells")
async def get_sells(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    sells = await sells_repository.get_all_by_account(db, account_id)
    return [{
        "id": sell.id,
        "stock": sell.stock,
        "date": sell.date,
        "shares": float(sell.shares),
        "transaction_amount": float(sell.transaction_amount),
        "profit": float(sell.profit),
        "proceeds": float(sell.proceeds),
        "adjusted_cost": float(sell.adjusted_cost)
    } for sell in sells]

@router.get("/accounts/{account_id}/net-profit")
async def get_net_profit(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    net_profit = await sells_repository.get_net_profit_by_account(db, account_id)
    return {"account_id": account_id, "net_profit": net_profit}

@router.get("/accounts/{account_id}/net-profit/by-year")
async def get_net_profit_by_year(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await sells_repository.get_net_profit_by_year(db, account_id)

@router.get("/accounts/{account_id}/net-profit/by-month")
async def get_net_profit_by_month(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await sells_repository.get_net_profit_by_month(db, account_id)

@router.get("/accounts/{account_id}/net-profit/by-stock")
async def get_net_profit_by_stock(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await sells_repository.get_net_profit_by_stock(db, account_id)
