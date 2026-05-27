import os
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()

# Sets PROJECT_ROOT to the fin-data-warehouse directory
PROJECT_ROOT_PATH = CURRENT_FILE.parent.parent.parent
LOCAL_STAGING_DIRECTORY_PATH = PROJECT_ROOT_PATH / 'data-staging'

class Config:
    STAGING_DIRECTORY = os.getenv('STAGING_DIRECTORY', str(LOCAL_STAGING_DIRECTORY_PATH))
    
    CALENDARS_CACHE_FILE = f'{STAGING_DIRECTORY}/trading_calendars'
    CALENDARS_END_DATE = '2026-12-31'

    TICKERS_INFO_FILE = f'{STAGING_DIRECTORY}/tickers_info.csv'

    NASDAQ_TICKERS_FILE = f'{STAGING_DIRECTORY}/nasdaq_tickers'
    NYSE_TICKERS_FILE = f'{STAGING_DIRECTORY}/nyse_tickers'
    WSE_TICKERS_FILE = f'{STAGING_DIRECTORY}/wse_tickers'
    TICKERS_CACHE_DAYS_VALID = 90


config = Config()
