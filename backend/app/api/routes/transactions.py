from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.stock_service import StockService
from app.services.file_service import FileService
from app.schemas.financial import FinancialAnalysisResponse, FinancialReport
from app.repositories.adjusted_cost_basis_repository import adjusted_cost_basis_repository
from app.db import get_db

router = APIRouter()

@router.post("/process-stock-transactions/{account_id}", response_model=FinancialAnalysisResponse)
async def process_stock_transactions(account_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        transactions = await FileService.extract_transactions_from_zip(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    financial_data = StockService.process_stock_transactions(transactions)
    
    await adjusted_cost_basis_repository.create_bulk(db, financial_data["sells"], account_id)
    
    return FinancialAnalysisResponse(
        status="processed",
        transactions_count=len(transactions),
        report=FinancialReport(
            net_profit_data=financial_data["net_profit_data"],
            dividend_data=financial_data["dividend_data"],
            interest_data=financial_data["interest_data"],
            sells=financial_data["sells"],
            formatted_report=financial_data["formatted_report"]
        )
    )