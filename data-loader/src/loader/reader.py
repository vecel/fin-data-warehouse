from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

from config import config


class ParquetReader:
    def resolve_glob(self, glob):
        return list(Path(config.STAGING_DIRECTORY).glob(glob))


    def modification_time(self, file):
        return datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc)


    def read(self, files):
        return pd.concat(
            [pd.read_parquet(f) for f in files],
            ignore_index=True,
        )
    
reader = ParquetReader()