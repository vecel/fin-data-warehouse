import logging

from datetime import datetime, timezone
import src.db.timestamps as timestamps
from src.loader.reader import TABLE_GLOBS, reader

logger = logging.getLogger(__name__)


def load_all(engine, force=False):
    logger.info('Loading .parquet files from staging directory')

    for table_name, glob in TABLE_GLOBS.items():
        _load_table(engine, table_name, glob, force)

    logger.info('Loading completed')


def _load_table(
    engine,
    table_name,
    glob,
    force
):
    files = reader.resolve_glob(glob)

    if not files:
        logger.warning(f'[{table_name}] no files found — skipping')
        return

    with engine.begin() as conn:
        timestamps.ensure_table(conn)
        last_loading_timestamp = timestamps.get_timestamp(conn, table_name)

    files = [file for file in files if force or not last_loading_timestamp or reader.modification_time(file) > last_loading_timestamp]

    logger.info(f'[{table_name}] loading {len(files)} file(s)')
    df = reader.read(files)

    with engine.begin() as conn:
        df.to_sql(
            name=table_name,
            con=conn,
            schema='stg',
            if_exists='append',
            index=False,
        )
        timestamps.set_timestamp(conn, table_name, datetime.now(timezone.utc))

    logger.info(f'[{table_name}] loaded {len(df):,} rows')