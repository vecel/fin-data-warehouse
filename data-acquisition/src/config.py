import os
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()

# Sets PROJECT_ROOT to the fin-data-warehouse directory
PROJECT_ROOT_PATH = CURRENT_FILE.parent.parent.parent
LOCAL_STAGING_DIRECTORY_PATH = PROJECT_ROOT_PATH / 'data-staging'

class Config:
    STAGING_DIRECTORY = os.getenv('STAGING_DIRECTORY', str(LOCAL_STAGING_DIRECTORY_PATH))

    NASDAQ_TICKERS_FILE = f'{STAGING_DIRECTORY}/nasdaq_tickers.txt'
    NYSE_TICKERS_FILE = f'{STAGING_DIRECTORY}/nyse_tickers.txt'
    WSE_TICKERS_FILE = f'{STAGING_DIRECTORY}/wse_tickers.txt'

    INSTRUMENT_DATA_FILE = f'{STAGING_DIRECTORY}/instrument_data.csv'

config = Config()
