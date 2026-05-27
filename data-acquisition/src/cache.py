import glob
import logging
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

from src.config import config

logger = logging.getLogger('cache')

class Cache:
    def __init__(self):
        cache_directory = Path(config.CACHE_DIRECTORY)
        cache_directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f'Ensured cache directory exists: {cache_directory}')


    def is_valid(self, filename, valid_days):
        files = self._get_cache_files(filename)
        if not files:
            logger.info(f'No cache files found for: {filename}')
            return False
        
        latest_file = self._get_latest_file(files)
        if len(files) > 1:
            logger.info(f'Multiple cache files found for {filename}. Removing older files.')
            for file in files:
                if file != latest_file:
                    self._remove_file(file)

        file_date = self._extract_date_from_filename(latest_file)
        
        if datetime.now() - file_date > timedelta(days=valid_days):
            logger.info(f'Cache expired. "{latest_file}" is older than {valid_days} days.')
            return False

        return True


    def load(self, filename):
        files = self._get_cache_files(filename)
        if not files:
            logger.info(f'No cache files found for: {filename}')
            return None
        
        latest_file = self._get_latest_file(files)

        if latest_file.endswith('.csv'):
            logger.info(f'Loading dataframe from cache: {latest_file}')
            return pd.read_csv(latest_file)
        elif latest_file.endswith('.txt'):
            logger.info(f'Loading list from cache: {latest_file}')
            with open(latest_file, 'r') as f:
                content = f.read()
                items = [line.strip() for line in content.split('\n') if line.strip()]
                return items
        else:
            logger.warning(f'Unsupported file format: {latest_file}')
            return None


    def save(self, data, filename):
        try:
            if isinstance(data, pd.DataFrame):
                file_path = self._append_date_to_filename(filename)
                data.to_csv(file_path + '.csv', index=False)
                logger.info(f'Saved dataframe to cache: {file_path}')
                return True
            
            elif isinstance(data, list):
                file_path = self._append_date_to_filename(filename)
                with open(file_path + '.txt', 'w') as f:
                    for item in data:
                        f.write(f'{item}\n')
                logger.info(f'Saved {len(data)} items to cache: {file_path}')
                return True
            
            else:
                logger.error(f'Unsupported data type: {type(data)}. Must be DataFrame or list.')
                return False
                
        except Exception as e:
            logger.error(f'Error saving cache {filename}: {e}')
            return False
    

    def _get_cache_files(self, filename: str) -> str:
        csv_pattern = f'{filename}-*.csv'
        txt_pattern = f'{filename}-*.txt'
        
        csv_files = glob.glob(csv_pattern)
        txt_files = glob.glob(txt_pattern)
        
        all_files = csv_files + txt_files
        return all_files


    def _get_latest_file(self, files):
        files.sort(reverse=True)
        return files[0] if files else None


    def _remove_file(self, path):
        try:
            os.remove(path)
            logger.info(f'Removed file: {path}')
        except Exception as e:
            logger.error(f'Error removing file {path}: {e}')


    def _append_date_to_filename(self, filename):
        date_str = datetime.now().strftime('%Y-%m-%d')
        return f'{filename}-{date_str}'


    def _extract_date_from_filename(self, filename: str):
        match = re.search(r'-(\d{4}-\d{2}-\d{2})\.', filename)
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y-%m-%d')
            except ValueError:
                logger.warning(f'Invalid date format in filename: {filename}')
                return None
        return None

cache = Cache()
