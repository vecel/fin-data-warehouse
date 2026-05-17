import os
import logging
from dotenv import load_dotenv

from src.fred_loader import load_fred_data
from src.ticker_loader import load_nasdaq_tickers, load_wse_tickers, load_nyse_tickers

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

if __name__ == "__main__":    
    logger = logging.getLogger('extract_data')
    logger.info('Starting data fetching script.')
    load_dotenv()

    FRED_KEY = os.getenv("FRED_API_KEY")

    if not FRED_KEY:
        raise ValueError("Missing key in .env file!")

    fred_df = load_fred_data(FRED_KEY)

    if not fred_df.empty:
        output_dir = os.getenv("CSV_OUTPUT_DIR", "../data-staging")
        os.makedirs(output_dir, exist_ok=True)
        
        csv_filename = os.path.join(output_dir, 'raw_fred_data.csv')
        fred_df.to_csv(csv_filename, index=False)
    else:
        print("FRED data frame is empty!")


    load_nasdaq_tickers()
    load_nyse_tickers()
    load_wse_tickers()