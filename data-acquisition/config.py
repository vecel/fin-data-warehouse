import os
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()

# Sets PROJECT_ROOT to the fin-data-warehouse directory
PROJECT_ROOT_PATH = CURRENT_FILE.parent.parent
LOCAL_STAGING_DIRECTORY_PATH = PROJECT_ROOT_PATH / 'staging'
LOCAL_CACHE_DIRECTORY_PATH = PROJECT_ROOT_PATH / 'cache'

class Config:
    STAGING_DIRECTORY = os.getenv('STAGING_DIRECTORY', str(LOCAL_STAGING_DIRECTORY_PATH))
    CACHE_DIRECTORY = os.getenv('CACHE_DIRECTORY', str(LOCAL_CACHE_DIRECTORY_PATH))
    
    CALENDARS_STAGING_FILE = f'{STAGING_DIRECTORY}/trading_calendars.parquet'
    COUNTRIES_STAGING_FILE = f'{STAGING_DIRECTORY}/countries.parquet'
    FUNDAMENTALS_STAGING_FILE = f'{STAGING_DIRECTORY}/fundamentals.parquet'

    TICKERS_CACHE_FILE = f'{CACHE_DIRECTORY}/tickers.parquet'

config = Config()
