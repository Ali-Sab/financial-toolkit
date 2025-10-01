from fastapi import UploadFile
from typing import List
from app.utils import validate_zip_file, extract_csv_files_from_zip, parse_csv_content

def get_currency_from_filename(filename):
    """Determine currency based on filename."""
    return 'USD' if 'USD' in filename else 'CAD'

class FileService:
    @staticmethod
    async def extract_transactions_from_zip(file: UploadFile) -> List[List[str]]:
        validate_zip_file(file)
        currency = get_currency_from_filename(file.filename)
        contents = await file.read()
        
        csv_contents = extract_csv_files_from_zip(contents)
        transactions = []
        
        for csv_content in csv_contents:
            rows = parse_csv_content(csv_content, currency)
            transactions.extend(rows)
        
        return transactions