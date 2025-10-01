from fastapi import APIRouter
from app.services.stock_service import StockService
from app.schemas.stock import StockResponse

router = APIRouter()

@router.get("/stocks", response_model=StockResponse)
def get_stocks():
    tickers = StockService.get_stock_tickers()
    return StockResponse(tickers=tickers)