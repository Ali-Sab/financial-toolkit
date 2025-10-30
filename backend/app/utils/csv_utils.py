import csv
import io
from typing import List
import logging

logger = logging.getLogger(__name__)

EXPECTED_HEADERS = ['date', 'transaction', 'description', 'amount', 'balance']

def validate_header_row(row: List[str]) -> bool:
    """Check if row has expected headers in order (first 5 columns)."""
    if len(row) < 5:
        return False
    
    for i, expected in enumerate(EXPECTED_HEADERS):
        if expected.lower() not in row[i].lower():
            return False
    
    return True

def parse_csv_content(csv_content: str, currency: str = "CAD") -> List[List[str]]:
    """Parse CSV content and return rows with currency appended if needed."""
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    
    if not rows:
        logger.warning("Empty CSV file encountered")
        return []
    
    # Check if first row is a valid header
    start_idx = 0
    has_currency_column = False
    
    if not validate_header_row(rows[0]):
        raise ValueError(f"Invalid CSV header. Expected columns: {', '.join(EXPECTED_HEADERS)}")
    
    start_idx = 1
    # Check if 6th column is currency
    if len(rows[0]) >= 6 and 'currency' in rows[0][5].lower():
        has_currency_column = True
        logger.info("CSV has currency column, using existing values")
    else:
        logger.info(f"CSV missing currency column, appending {currency}")
    
    # Process data rows - take first 5 columns, add currency if needed
    result = []
    for row in rows[start_idx:]:
        if len(row) < 5:
            continue
        
        # Take first 5 columns
        data_row = row[:5]
        
        # Add currency from 6th column or default
        if has_currency_column and len(row) >= 6:
            data_row.append(row[5])
        else:
            data_row.append(currency)
        
        result.append(data_row)
    
    return result