from pathlib import Path
import pandas as pd
import logging


logger = logging.getLogger(__name__)

class ParquetWriter:
    def read(self, src: str) -> pd.DataFrame:
        src_path = Path(src)
        if not src_path.exists():
            raise FileNotFoundError(f'File {src} does not exist.')
        return pd.read_parquet(src)

    def write(self, df: pd.DataFrame, dest: str) -> None:
        dest_path = Path(dest)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest_path.with_suffix('.tmp.parquet')

        try:
            df.to_parquet(tmp, index=False, engine='pyarrow', compression='snappy')
            tmp.rename(dest_path)
        except Exception as e:
            tmp.unlink(missing_ok=True)
            raise RuntimeError(f'Failed writing {dest}: {e}')
        
writer = ParquetWriter()