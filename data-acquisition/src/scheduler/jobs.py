import logging
from pathlib import Path

from src.fetchers.calendars import fetch_trading_calendars
from src.fetchers.countries import fetch_countries
from src.fetchers.tickers import fetch_tickers
from src.fetchers.fundamentals import fetch_fundamentals
from src.writer.parquet_writer import writer
from config import config


logger = logging.getLogger(__name__)

def _exists(file):
    return Path(file).exists()

def bootstrap_job():
    if not _exists(config.COUNTRIES_STAGING_FILE):
        countries = fetch_countries()
        writer.write(countries, config.COUNTRIES_STAGING_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(countries)} countries to {config.COUNTRIES_STAGING_FILE}')

    if not _exists(config.CALENDARS_STAGING_FILE):
        calendars = fetch_trading_calendars()
        writer.write(calendars, config.CALENDARS_STAGING_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(calendars)} trading calendar dates to {config.CALENDARS_STAGING_FILE}')
    
    if not _exists(config.TICKERS_CACHE_FILE):
        tickers = fetch_tickers()
        writer.write(tickers, config.TICKERS_CACHE_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(tickers)} tickers to {config.TICKERS_CACHE_FILE}')

    if not _exists(config.FUNDAMENTALS_STAGING_FILE):
        tickers = writer.read(config.TICKERS_CACHE_FILE)
        tickers = tickers['ticker'].tolist()
        fundamentals = fetch_fundamentals(tickers)
        writer.write(fundamentals, config.FUNDAMENTALS_STAGING_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(fundamentals)} fundamentals to {config.FUNDAMENTALS_STAGING_FILE}')


def calendars_annual_job():
    calendars = fetch_trading_calendars()
    writer.write(calendars, config.CALENDARS_STAGING_FILE)
    logger.info('Annual job completed: calendars data fetched and saved to staging.')

def fundamentals_monthly_job():
    try:
        tickers = writer.read(config.TICKERS_CACHE_FILE)
        tickers = tickers['ticker'].tolist()
    except FileNotFoundError:
        raise RuntimeError(f'Tickers cache file not found at {config.TICKERS_CACHE_FILE}. Please run the bootstrap job first.')

    fundamentals = fetch_fundamentals(tickers)
    writer.write(fundamentals, config.FUNDAMENTALS_STAGING_FILE)
    logger.info('Monthly job completed: fundamentals data fetched and saved to staging.')
