from fastapi import UploadFile
from typing import List
import logging
from app.utils import validate_zip_file, extract_csv_files_from_zip, parse_csv_content

logger = logging.getLogger(__name__)

def get_currency_from_filename(filename: str) -> str:
    """Determine currency based on filename."""
    currency = 'USD' if 'USD' in filename.upper() else 'CAD'
    logger.info(f"Detected currency: {currency} for {filename}")
    return currency

class FileService:
    @staticmethod
    async def extract_transactions_from_zip(file: UploadFile) -> List[List[str]]:
        validate_zip_file(file)
        contents = await file.read()
        
        csv_files = extract_csv_files_from_zip(contents)
        transactions = []
        
        for filename, csv_content in csv_files:
            currency = get_currency_from_filename(filename)
            rows = parse_csv_content(csv_content, currency)
            transactions.extend(rows)
        
        return transactions