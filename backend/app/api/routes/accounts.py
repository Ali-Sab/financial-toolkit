from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.db.models import User
from app.utils.auth_utils import get_current_user
from app.repositories.account_repository import account_repository
from pydantic import BaseModel

router = APIRouter()

class AccountCreate(BaseModel):
    account_name: str
    account_type: str

class AccountUpdate(BaseModel):
    account_name: str | None = None
    account_type: str | None = None

@router.post("/accounts")
async def create_account(
    account_data: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    account = await account_repository.create(db, account_data.account_name, account_data.account_type, current_user.id)
    return {"id": account.id, "account_name": account.account_name, "account_type": account.account_type}

@router.get("/accounts")
async def get_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    accounts = await account_repository.get_all_by_user(db, current_user.id)
    return [{"id": acc.id, "account_name": acc.account_name, "account_type": acc.account_type} for acc in accounts]

@router.get("/accounts/{account_id}")
async def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    account = await account_repository.get_by_id(db, account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"id": account.id, "account_name": account.account_name, "account_type": account.account_type}

@router.put("/accounts/{account_id}")
async def update_account(
    account_id: int,
    account_data: AccountUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    account = await account_repository.get_by_id(db, account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account = await account_repository.update(db, account, account_data.account_name, account_data.account_type)
    return {"id": account.id, "account_name": account.account_name, "account_type": account.account_type}

@router.delete("/accounts/{account_id}")
async def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    account = await account_repository.get_by_id(db, account_id, current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    await account_repository.delete(db, account)
    return {"message": "Account deleted"}
