from pydantic import BaseModel
from typing import List

class TransactionRequest(BaseModel):
    transactions: List[List[str]]