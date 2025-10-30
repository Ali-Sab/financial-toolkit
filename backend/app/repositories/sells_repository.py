from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from app.db.models import AdjustedCostBasisSell

class SellsRepository:
    async def get_all_by_account(self, db: AsyncSession, account_id: int) -> list[AdjustedCostBasisSell]:
        result = await db.execute(
            select(AdjustedCostBasisSell).where(AdjustedCostBasisSell.financial_account_id == account_id)
        )
        return list(result.scalars().all())
    
    async def get_net_profit_by_account(self, db: AsyncSession, account_id: int) -> float:
        result = await db.execute(
            select(func.sum(AdjustedCostBasisSell.profit)).where(
                AdjustedCostBasisSell.financial_account_id == account_id
            )
        )
        total = result.scalar()
        return float(total) if total else 0.0
    
    async def get_net_profit_by_year(self, db: AsyncSession, account_id: int) -> list[dict]:
        result = await db.execute(
            select(
                extract('year', AdjustedCostBasisSell.date).label('year'),
                func.sum(AdjustedCostBasisSell.profit).label('profit')
            ).where(
                AdjustedCostBasisSell.financial_account_id == account_id
            ).group_by('year').order_by('year')
        )
        return [{'year': int(row.year), 'profit': float(row.profit)} for row in result]
    
    async def get_net_profit_by_month(self, db: AsyncSession, account_id: int) -> list[dict]:
        result = await db.execute(
            select(
                extract('year', AdjustedCostBasisSell.date).label('year'),
                extract('month', AdjustedCostBasisSell.date).label('month'),
                func.sum(AdjustedCostBasisSell.profit).label('profit')
            ).where(
                AdjustedCostBasisSell.financial_account_id == account_id
            ).group_by('year', 'month').order_by('year', 'month')
        )
        return [{'year': int(row.year), 'month': int(row.month), 'profit': float(row.profit)} for row in result]
    
    async def get_net_profit_by_stock(self, db: AsyncSession, account_id: int) -> list[dict]:
        result = await db.execute(
            select(
                AdjustedCostBasisSell.stock,
                func.sum(AdjustedCostBasisSell.profit).label('profit')
            ).where(
                AdjustedCostBasisSell.financial_account_id == account_id
            ).group_by(AdjustedCostBasisSell.stock).order_by(func.sum(AdjustedCostBasisSell.profit).desc())
        )
        return [{'stock': row.stock, 'profit': float(row.profit)} for row in result]

sells_repository = SellsRepository()
