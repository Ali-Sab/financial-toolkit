from pydantic import BaseModel
from typing import List

class StockResponse(BaseModel):
    tickers: List[str]