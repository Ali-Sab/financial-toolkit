from fastapi import APIRouter, File, UploadFile
from app.services.stock_service import StockService
from app.services.file_service import FileService
from app.schemas.financial import FinancialAnalysisResponse, FinancialReport

router = APIRouter()

@router.post("/process-stock-transactions/", response_model=FinancialAnalysisResponse)
async def process_stock_transactions(file: UploadFile = File(...)):
    transactions = await FileService.extract_transactions_from_zip(file)
    financial_data = StockService.process_stock_transactions(transactions)
    
    return FinancialAnalysisResponse(
        status="processed",
        transactions_count=len(transactions),
        report=FinancialReport(
            net_profit_data=financial_data["net_profit_data"],
            dividend_data=financial_data["dividend_data"],
            interest_data=financial_data["interest_data"],
            formatted_report=financial_data["formatted_report"]
        )
    )