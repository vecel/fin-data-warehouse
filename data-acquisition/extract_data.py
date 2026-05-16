import os
from dotenv import load_dotenv

from src.fred_loader import load_fred_data

if __name__ == "__main__":
    load_dotenv()

    FRED_KEY = os.getenv("FRED_API_KEY")

    if not FRED_KEY:
        raise ValueError("Missing key in .env file!")

    # Loading FRED data
    fred_df = load_fred_data(FRED_KEY)

    # Load df to db