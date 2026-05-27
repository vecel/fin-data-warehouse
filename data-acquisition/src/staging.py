import logging
from pathlib import Path
import pandas as pd

from src.config import config

logger = logging.getLogger('staging')


class Staging:
    def __init__(self):
        staging_directory = Path(config.STAGING_DIRECTORY)
        staging_directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f'Ensured staging directory exists: {staging_directory}')

    def save(self, data, filename):
        if not isinstance(data, pd.DataFrame):
            logger.error('Staging.save only supports pandas.DataFrame objects.')
            return False

        try:
            data.to_csv(filename, index=False)
            logger.info(f'Saved staged data to {filename}')
            return True
        except Exception as e:
            logger.error(f'Failed to save staged data to {filename}: {e}')
            return False
        
staging = Staging()