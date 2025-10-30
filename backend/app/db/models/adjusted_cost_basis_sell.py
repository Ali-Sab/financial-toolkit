from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class AdjustedCostBasisSell(Base):
    __tablename__ = "adjusted_cost_basis_sells"

    id = Column(Integer, primary_key=True, index=True)
    stock = Column(String, nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    shares = Column(Numeric(20, 8), nullable=False)
    transaction_amount = Column(Numeric(20, 8), nullable=False)
    profit = Column(Numeric(20, 8), nullable=False)
    proceeds = Column(Numeric(20, 8), nullable=False)
    adjusted_cost = Column(Numeric(20, 8), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    financial_account_id = Column(Integer, ForeignKey("financial_accounts.id", ondelete="CASCADE"), nullable=False)
    financial_account = relationship("FinancialAccount", back_populates="sells")

