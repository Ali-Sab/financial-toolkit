from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AdjustedCostBasisSell
from datetime import date

class AdjustedCostBasisRepository:
    async def create_bulk(self, db: AsyncSession, sells: list[dict], financial_account_id: int) -> list[AdjustedCostBasisSell]:
        records = []
        for sell in sells:
            record = AdjustedCostBasisSell(
                stock=sell['stock'],
                date=sell['date'],
                shares=sell['transaction.shares'],
                transaction_amount=sell['transaction_amount'],
                profit=sell['profit'],
                proceeds=sell['proceeds'],
                adjusted_cost=sell['adjusted_cost'],
                financial_account_id=financial_account_id
            )
            db.add(record)
            records.append(record)
        
        await db.commit()
        return records

adjusted_cost_basis_repository = AdjustedCostBasisRepository()
