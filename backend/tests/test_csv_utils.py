import pytest
from app.utils.csv_utils import is_header_row, parse_csv_content

def test_is_header_row():
    assert is_header_row(["Date", "Symbol", "Quantity", "Price", "Type"]) == True
    assert is_header_row(["2023-01-01", "AAPL", "100", "150.00", "BUY"]) == False  # No letters in date
    assert is_header_row(["123", "456", "789", "000", "111"]) == False
    assert is_header_row(["01/01/2023", "AAPL", "100", "150.00", "BUY"]) == False  # No letters in first cell
    assert is_header_row(["Jan-01-2023", "AAPL", "100", "150.00", "BUY"]) == True  # Has letters in date

def test_parse_csv_content_with_headers():
    csv_content = "Date,Symbol,Quantity,Price,Type\n2023-01-01,AAPL,100,150.00,BUY\n2023-01-02,GOOGL,50,2500.00,SELL"
    result = parse_csv_content(csv_content)
    expected = [
        ["2023-01-01", "AAPL", "100", "150.00", "BUY", "CAD"],
        ["2023-01-02", "GOOGL", "50", "2500.00", "SELL", "CAD"]
    ]
    assert result == expected

def test_parse_csv_content_without_headers():
    csv_content = "2023-01-01,AAPL,100,150.00,BUY\n2023-01-02,GOOGL,50,2500.00,SELL"
    result = parse_csv_content(csv_content)
    expected = [
        ["2023-01-01", "AAPL", "100", "150.00", "BUY", "CAD"],
        ["2023-01-02", "GOOGL", "50", "2500.00", "SELL", "CAD"]
    ]
    assert result == expected

def test_parse_csv_content_filters_wrong_columns():
    csv_content = "Date,Symbol,Quantity,Price,Type\n2023-01-01,AAPL,100,150.00,BUY\n2023-01-02,GOOGL,50\n2023-01-03,MSFT,75,300.00,BUY"
    result = parse_csv_content(csv_content)
    expected = [
        ["2023-01-01", "AAPL", "100", "150.00", "BUY", "CAD"],
        ["2023-01-03", "MSFT", "75", "300.00", "BUY", "CAD"]
    ]
    assert result == expected

def test_parse_csv_content_custom_currency():
    csv_content = "2023-01-01,AAPL,100,150.00,BUY"
    result = parse_csv_content(csv_content, currency="USD")
    expected = [
        ["2023-01-01", "AAPL", "100", "150.00", "BUY", "USD"]
    ]
    assert result == expected