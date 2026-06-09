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
    
    CALENDARS_STAGING_FILE = f'{STAGING_DIRECTORY}/calendars.parquet'
    COUNTRIES_STAGING_FILE = f'{STAGING_DIRECTORY}/countries.parquet'

    MACRO_STAGING_FILE = f'{STAGING_DIRECTORY}/macro.parquet'
    QUOTES_STAGING_FILE = f'{STAGING_DIRECTORY}/quotes.parquet'
    NEWS_STAGING_FILE = f'{STAGING_DIRECTORY}/news.parquet'

    WSE_FUNDAMENTALS_STAGING_FILE = f'{STAGING_DIRECTORY}/wse_fundamentals.parquet'
    NASDAQ_FUNDAMENTALS_STAGING_FILE = f'{STAGING_DIRECTORY}/nasdaq_fundamentals.parquet'
    NYSE_FUNDAMENTALS_STAGING_FILE = f'{STAGING_DIRECTORY}/nyse_fundamentals.parquet'

    WSE_TICKERS_CACHE_FILE = f'{CACHE_DIRECTORY}/wse_tickers.parquet'
    NASDAQ_TICKERS_CACHE_FILE = f'{CACHE_DIRECTORY}/nasdaq_tickers.parquet'
    NYSE_TICKERS_CACHE_FILE = f'{CACHE_DIRECTORY}/nyse_tickers.parquet'

config = Config()
