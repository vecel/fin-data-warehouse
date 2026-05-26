import glob
import logging
import re
from datetime import datetime, timedelta

from src.config import config

logger = logging.getLogger('cache')

def save_tickers(tickers, filename):
    today_str = datetime.now().strftime('%Y-%m-%d')
    path = f'{filename}-{today_str}.txt'
    
    with open(path, 'w') as file:
        for ticker in tickers:
            file.write(f'{ticker}\n')
        
    logger.info(f'Saved {len(tickers)} tickers to {path}.')

def load_tickers_cache(filename):
    pattern = f'{filename}-*.txt'
    matching_files = glob.glob(pattern)
    
    if not matching_files:
        logger.info(f'No cache files found for {filename}.')
        return None

    matching_files.sort(reverse=True)
    latest_file = matching_files[0]
    
    match = re.search(r'-(\d{4}-\d{2}-\d{2})\.txt$', latest_file)
    if not match:
        logger.warning(f'Could not parse date for {filename}.')
        return None
        
    date_str = match.group(1)
    file_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    if datetime.now() - file_date > timedelta(days=config.TICKERS_CACHE_DAYS_VALID):
        logger.info(f'Cache expired. "{latest_file}" is older than {config.TICKERS_CACHE_DAYS_VALID} days.')
        return None
        
    logger.info(f'Reading tickers data from cache: {latest_file}')
    with open(latest_file, 'r') as file:
        content = file.read()
        tickers = content.split('\n')[:-1]
        return tickers