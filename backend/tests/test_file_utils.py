import pytest
import zipfile
import io
from fastapi import HTTPException
from unittest.mock import Mock
from app.utils.file_utils import validate_zip_file, extract_csv_files_from_zip

def test_validate_zip_file_valid():
    mock_file = Mock()
    mock_file.filename = "test.zip"
    validate_zip_file(mock_file)  # Should not raise

def test_validate_zip_file_invalid():
    mock_file = Mock()
    mock_file.filename = "test.txt"
    with pytest.raises(HTTPException) as exc_info:
        validate_zip_file(mock_file)
    assert exc_info.value.status_code == 400

def test_extract_csv_files_from_zip():
    # Create a test ZIP with CSV content
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr("data1.csv", "col1,col2\nval1,val2")
        zip_file.writestr("data2.csv", "col3,col4\nval3,val4")
        zip_file.writestr("readme.txt", "This is not a CSV")
    
    zip_content = zip_buffer.getvalue()
    result = extract_csv_files_from_zip(zip_content)
    
    assert len(result) == 2
    assert "col1,col2\nval1,val2" in result
    assert "col3,col4\nval3,val4" in result

def test_extract_csv_files_from_invalid_zip():
    invalid_zip_content = b"not a zip file"
    with pytest.raises(HTTPException) as exc_info:
        extract_csv_files_from_zip(invalid_zip_content)
    assert exc_info.value.status_code == 400