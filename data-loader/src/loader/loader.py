import logging

from datetime import datetime, timezone
import src.db.db as db
from src.loader.reader import reader
from config import config

logger = logging.getLogger(__name__)


def load_all(engine, force=False):
    logger.info('Loading .parquet files from staging directory')

    for table_name, glob in config.STAGING_GLOBS.items():
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
        db.ensure_timestamps_table(conn)
        last_loading_timestamp = db.get_timestamp(conn, table_name)

    files = [file for file in files if force or not last_loading_timestamp or reader.modification_time(file) > last_loading_timestamp]

    if not files:
        logger.info(f'[{table_name}] no new files to load — skipping')
        return

    df = reader.read(files)

    with engine.begin() as conn:
        logger.info(f'[{table_name}] upserting {len(files)} file(s)')
        db.ensure_table(conn, table_name, df, config.PRIMARY_KEYS[table_name])
        db.upsert(conn, table_name, df, config.PRIMARY_KEYS[table_name])
        db.set_timestamp(conn, table_name, datetime.now(timezone.utc))

    logger.info(f'[{table_name}] upserted {len(df):,} rows')