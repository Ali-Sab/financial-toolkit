from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class FinancialAccount(Base):
    __tablename__ = "financial_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)  # e.g., "TFSA", "RRSP", "Taxable"
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="financial_accounts")
    sells = relationship("AdjustedCostBasisSell", back_populates="financial_account")

