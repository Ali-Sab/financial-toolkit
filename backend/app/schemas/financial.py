from pydantic import BaseModel
from typing import List

class NetProfitEntry(BaseModel):
    year: int
    stock: str
    net_profit: float

class DividendEntry(BaseModel):
    year: int
    stock: str
    dividends: float

class InterestEntry(BaseModel):
    year: int
    interest: float

class FinancialReport(BaseModel):
    net_profit_data: List[NetProfitEntry]
    dividend_data: List[DividendEntry]
    interest_data: List[InterestEntry]
    formatted_report: str

class FinancialAnalysisResponse(BaseModel):
    status: str
    transactions_count: int
    report: FinancialReport