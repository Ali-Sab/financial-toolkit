import csv
import io
from typing import List

def is_header_row(row: List[str]) -> bool:
    """Check if a row contains headers by checking first cell for alphabetic characters."""
    return bool(row and any(c.isalpha() for c in row[0]))

def parse_csv_content(csv_content: str, currency: str = "CAD", expected_columns: int = 5) -> List[List[str]]:
    """Parse CSV content and return rows with currency appended, skipping headers if detected."""
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    
    if not rows:
        return []
    
    # Skip header if first row contains letters and has expected columns
    start_idx = 0
    if len(rows[0]) == expected_columns and is_header_row(rows[0]):
        start_idx = 1
    
    return [row + [currency] for row in rows[start_idx:] if len(row) == expected_columns]