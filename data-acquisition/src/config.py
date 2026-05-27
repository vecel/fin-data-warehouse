import os
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()

# Sets PROJECT_ROOT to the fin-data-warehouse directory
PROJECT_ROOT_PATH = CURRENT_FILE.parent.parent.parent
LOCAL_STAGING_DIRECTORY_PATH = PROJECT_ROOT_PATH / 'data-staging'
LOCAL_CACHE_DIRECTORY_PATH = PROJECT_ROOT_PATH / 'cache'

class Config:
    STAGING_DIRECTORY = os.getenv('STAGING_DIRECTORY', str(LOCAL_STAGING_DIRECTORY_PATH))
    CACHE_DIRECTORY = os.getenv('CACHE_DIRECTORY', str(LOCAL_CACHE_DIRECTORY_PATH))
    
    CALENDARS_CACHE = f'{CACHE_DIRECTORY}/trading_calendars'
    CALENDARS_STAGING_FILE = f'{STAGING_DIRECTORY}/trading_calendars.csv'
    CALENDARS_CACHE_DAYS_VALID = 365
    CALENDARS_END_DATE = '2026-12-31'

    NASDAQ_TICKERS_CACHE = f'{CACHE_DIRECTORY}/nasdaq_tickers'
    NYSE_TICKERS_CACHE = f'{CACHE_DIRECTORY}/nyse_tickers'
    WSE_TICKERS_CACHE = f'{CACHE_DIRECTORY}/wse_tickers'
    TICKERS_CACHE_DAYS_VALID = 365

    WSE_INFO_CACHE = f'{CACHE_DIRECTORY}/wse_tickers_info'
    WSE_INFO_STAGING_FILE = f'{STAGING_DIRECTORY}/wse_tickers_info.csv'
    TICKERS_INFO_CACHE_DAYS_VALID = 30



config = Config()
