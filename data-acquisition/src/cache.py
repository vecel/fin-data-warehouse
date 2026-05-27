import glob
import logging
import re
from datetime import datetime, timedelta

from src.config import config

logger = logging.getLogger('cache')

def save_calendars(dataframe, end_date):   
    try: 
        dataframe.to_csv(f'{config.CALENDARS_CACHE_FILE}-{end_date}.csv', index=False)
        logger.info(f'Saved market calendars to cache: {config.CALENDARS_CACHE_FILE}-{end_date}.csv')
    except PermissionError as e:
        logger.error(f'Could not write market calendars to cache {config.CALENDARS_CACHE_FILE}-{end_date}.csv, because of PermissionError: {e}')

def is_calendars_cache_valid():
    pattern = f'{config.CALENDARS_CACHE_FILE}-*.csv'

    latest_file, file_date = _get_latest_file_for_pattern(pattern)
    if not latest_file:
        return False
    
    if datetime.now() > file_date:
        logger.info(f'Calendars cache expired. "{latest_file}" is older than current date.')
        return False
    
    return True

def save_tickers(tickers, filename):
    today_str = datetime.now().strftime('%Y-%m-%d')
    path = f'{filename}-{today_str}.txt'
    
    with open(path, 'w') as file:
        for ticker in tickers:
            file.write(f'{ticker}\n')
        
    logger.info(f'Saved {len(tickers)} tickers to {path}.')

def load_tickers_cache(filename):
    pattern = f'{filename}-*.txt'
    
    latest_file, file_date = _get_latest_file_for_pattern(pattern)
    if not latest_file:
        return None
    
    if datetime.now() - file_date > timedelta(days=config.TICKERS_CACHE_DAYS_VALID):
        logger.info(f'Cache expired. "{latest_file}" is older than {config.TICKERS_CACHE_DAYS_VALID} days.')
        return None
        
    logger.info(f'Reading tickers data from cache: {latest_file}')
    with open(latest_file, 'r') as file:
        content = file.read()
        tickers = content.split('\n')[:-1]
        return tickers
    
def _get_latest_file_for_pattern(pattern):
    matching_files = glob.glob(pattern)
    
    if not matching_files:
        logger.info(f'No cache found for {pattern}.')
        return None, None

    matching_files.sort(reverse=True)
    latest_file = matching_files[0]
    
    match = re.search(r'-(\d{4}-\d{2}-\d{2})\.', latest_file)
    if not match:
        logger.warning(f'Could not parse date for {pattern}.')
        return None, None
        
    date_str = match.group(1)
    file_date = datetime.strptime(date_str, '%Y-%m-%d')

    return latest_file, file_date
