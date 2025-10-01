import zipfile
import io
from fastapi import HTTPException, UploadFile
from typing import List

def validate_zip_file(file: UploadFile) -> None:
    """Validate that uploaded file is a ZIP file."""
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="File must be a ZIP file")

def extract_csv_files_from_zip(zip_content: bytes) -> List[str]:
    """Extract CSV file contents from ZIP."""
    csv_contents = []
    try:
        with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_file:
            for filename in zip_file.namelist():
                if filename.endswith('.csv'):
                    csv_content = zip_file.read(filename).decode('utf-8')
                    csv_contents.append(csv_content)
        return csv_contents
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP file")