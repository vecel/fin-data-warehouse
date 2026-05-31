import os
import logging
import argparse
import pandas as pd
from dotenv import load_dotenv

# from src.config import config
from src.scheduler.scheduler import build
# from src.cache import cache
# from src.staging import staging
# from src.ticker_loader import fetch_nasdaq_tickers, fetch_wse_tickers, fetch_nyse_tickers
# from src.calendar_loader import get_trading_calendars
# from src.country_loader import get_countries
# from src.fred_loader import load_fred_data
# from src.quote_loader import fetch_tickers_info

parser = argparse.ArgumentParser()
parser.add_argument(
    '-v',
    '--verbose',
    default='INFO',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help='Set logging level (default: INFO)',
)
args = parser.parse_args()

logging.basicConfig(
    level=getattr(logging, args.verbose),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":  
    scheduler = build()
    scheduler.start()
    # if cache.is_valid(config.WSE_TICKERS_CACHE, config.TICKERS_CACHE_DAYS_VALID):
    #     wse_tickers = cache.load(config.WSE_TICKERS_CACHE)
    # else:
    #     wse_tickers = fetch_wse_tickers()
    #     if wse_tickers:
    #         cache.save(wse_tickers, config.WSE_TICKERS_CACHE)  



    # if cache.is_valid(config.CALENDARS_CACHE, valid_days=config.CALENDARS_CACHE_DAYS_VALID):
    #     calendars = cache.load(config.CALENDARS_CACHE)
    # else:
    #     calendars = get_trading_calendars(end_date=config.CALENDARS_END_DATE)
    #     cache.save(calendars, config.CALENDARS_CACHE)
    # staging.save(calendars, config.CALENDARS_STAGING_FILE)


    # countires = get_countries()
    # staging.save(countires, config.COUNTRIES_STAGING_FILE)
    
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


    # Fetch tickers info, comment if you do not want - it takes a while.
    # WSE_DELISTED = ['REX.WA', 'KDM.WA', 'IDG.WA', 'REG.WA', 'SVR.WA']
    # if cache.is_valid(config.WSE_TICKERS_INFO_CACHE, config.TICKERS_INFO_CACHE_DAYS_VALID):
    #     wse_tickers_info = cache.load(config.WSE_TICKERS_INFO_CACHE)
    # else:
    #     listed_wse_tickers = [ticker for ticker in wse_tickers if ticker not in WSE_DELISTED]
    #     wse_tickers_info = fetch_tickers_info(listed_wse_tickers)
    #     cache.save(wse_tickers_info, config.WSE_TICKERS_INFO_CACHE)

    # staging.save(wse_tickers_info, config.WSE_TICKERS_INFO_STAGING_FILE)

    # df = pd.DataFrame(wse_tickers_info)
    # df.to_csv(config.TICKERS_INFO_FILE, index=False)

    # load_nasdaq_tickers()
    # load_nyse_tickers()
    # load_wse_tickers()