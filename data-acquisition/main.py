import os
import logging
import pandas as pd
from dotenv import load_dotenv

from src.config import config
from src.cache import load_tickers_cache, save_tickers
from src.fred_loader import load_fred_data
from src.ticker_loader import fetch_nasdaq_tickers, fetch_wse_tickers, fetch_nyse_tickers
from src.quote_loader import fetch_tickers_info

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

if __name__ == "__main__":    
    # fetch_instrument_data(config.INSTRUMENT_DATA_FILE)
    logger = logging.getLogger('main')
    # logger.info('Starting data fetching script.')
    # load_dotenv()

    # FRED_KEY = os.getenv("FRED_API_KEY")

    # if not FRED_KEY:
    #     raise ValueError("Missing key in .env file!")

    # fred_df = load_fred_data(FRED_KEY)

    # if not fred_df.empty:
    #     output_dir = os.getenv("CSV_OUTPUT_DIR", "../data-staging")
    #     os.makedirs(output_dir, exist_ok=True)
        
    #     csv_filename = os.path.join(output_dir, 'raw_fred_data.csv')
    #     fred_df.to_csv(csv_filename, index=False)
    # else:
    #     print("FRED data frame is empty!")

    WSE_DELISTED = ['REX.WA', 'KDM.WA', 'IDG.WA', 'REG.WA', 'SVR.WA']

    wse_tickers = load_tickers_cache(config.WSE_TICKERS_FILE)
    if not wse_tickers:
        wse_tickers = fetch_wse_tickers()
        if wse_tickers:
            save_tickers(wse_tickers, config.WSE_TICKERS_FILE)

    # Fetch tickers info, comment if you do not want - it takes a while.
    # wse_tickers = [ticker for ticker in wse_tickers if ticker not in WSE_DELISTED]
    # wse_tickers_info = fetch_tickers_info(wse_tickers)

    # df = pd.DataFrame(wse_tickers_info)
    # df.to_csv(config.TICKERS_INFO_FILE, index=False)

    # load_nasdaq_tickers()
    # load_nyse_tickers()
    # load_wse_tickers()