from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import FinancialAccount

class AccountRepository:
    async def get_by_id(self, db: AsyncSession, account_id: int, user_id: int) -> FinancialAccount | None:
        result = await db.execute(
            select(FinancialAccount).where(
                FinancialAccount.id == account_id,
                FinancialAccount.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_all_by_user(self, db: AsyncSession, user_id: int) -> list[FinancialAccount]:
        result = await db.execute(
            select(FinancialAccount).where(FinancialAccount.user_id == user_id)
        )
        return list(result.scalars().all())
    
    async def create(self, db: AsyncSession, account_name: str, account_type: str, user_id: int) -> FinancialAccount:
        account = FinancialAccount(account_name=account_name, account_type=account_type, user_id=user_id)
        db.add(account)
        await db.commit()
        await db.refresh(account)
        return account
    
    async def update(self, db: AsyncSession, account: FinancialAccount, account_name: str | None, account_type: str | None) -> FinancialAccount:
        if account_name is not None:
            account.account_name = account_name
        if account_type is not None:
            account.account_type = account_type
        await db.commit()
        await db.refresh(account)
        return account
    
    async def delete(self, db: AsyncSession, account: FinancialAccount) -> None:
        await db.delete(account)
        await db.commit()

account_repository = AccountRepository()
