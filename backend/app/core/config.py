from pathlib import Path

# Get the app directory path
APP_DIR = Path(__file__).parent.parent
DATA_DIR = APP_DIR / "data"

# Exchange rates file path
USD_TO_CAD_RATES_FILE = DATA_DIR / "usd-to-cad-rates.csv"