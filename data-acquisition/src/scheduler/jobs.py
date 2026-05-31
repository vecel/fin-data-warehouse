import logging
from pathlib import Path

from src.fetchers.calendars import fetch_trading_calendars
from src.fetchers.countries import fetch_countries
from src.fetchers.tickers import (
    fetch_nasdaq_tickers, 
    fetch_nyse_tickers,
    fetch_wse_tickers
)
from src.fetchers.fundamentals import fetch_fundamentals
from src.writer.parquet_writer import writer
from config import config


logger = logging.getLogger(__name__)

def _exists(file):
    return Path(file).exists()


def _fetch_fundamentals(cache_file):
    try:
        tickers_df = writer.read(cache_file)
    except FileNotFoundError:
        raise RuntimeError(f'Tickers cache file not found at {cache_file}. Please run the bootstrap job first.')

    tickers = tickers_df['ticker'].tolist()
    fundamentals = fetch_fundamentals(tickers)
    return fundamentals


def bootstrap_job():
    if not _exists(config.COUNTRIES_STAGING_FILE):
        countries = fetch_countries()
        writer.write(countries, config.COUNTRIES_STAGING_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(countries)} countries to {config.COUNTRIES_STAGING_FILE}.')

    if not _exists(config.CALENDARS_STAGING_FILE):
        calendars = fetch_trading_calendars()
        writer.write(calendars, config.CALENDARS_STAGING_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(calendars)} trading calendar dates to {config.CALENDARS_STAGING_FILE}.')
    
    if not _exists(config.WSE_TICKERS_CACHE_FILE):
        wse_delisted = ['REX.WA', 'KDM.WA', 'IDG.WA', 'REG.WA', 'SVR.WA']
        wse_tickers = fetch_wse_tickers()
        wse_tickers = [ticker for ticker in wse_tickers if ticker not in wse_delisted]
        writer.write(wse_tickers, config.WSE_TICKERS_CACHE_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(wse_tickers)} WSE tickers to {config.WSE_TICKERS_CACHE_FILE}.')

    if not _exists(config.NASDAQ_TICKERS_CACHE_FILE):
        nasdaq_tickers = fetch_nasdaq_tickers()
        writer.write(nasdaq_tickers, config.NASDAQ_TICKERS_CACHE_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(nasdaq_tickers)} Nasdaq tickers to {config.NASDAQ_TICKERS_CACHE_FILE}.')

    if not _exists(config.NYSE_TICKERS_CACHE_FILE):
        nyse_tickers = fetch_nyse_tickers()
        writer.write(nyse_tickers, config.NYSE_TICKERS_CACHE_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(nyse_tickers)} Nyse tickers to {config.NYSE_TICKERS_CACHE_FILE}.')

    if not _exists(config.WSE_FUNDAMENTALS_STAGING_FILE):
        fundamentals = _fetch_fundamentals(config.WSE_TICKERS_CACHE_FILE)
        writer.write(fundamentals, config.WSE_FUNDAMENTALS_STAGING_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(fundamentals)} fundamentals to {config.WSE_FUNDAMENTALS_STAGING_FILE}.')


def calendars_annual_job():
    calendars = fetch_trading_calendars()
    writer.write(calendars, config.CALENDARS_STAGING_FILE)
    logger.info(f'Annual job completed: {len(calendars)} calendars data fetched and saved to {config.CALENDARS_STAGING_FILE}.')


def wse_fundamentals_monthly_job():
    fundamentals = _fetch_fundamentals(config.WSE_TICKERS_CACHE_FILE)
    writer.write(fundamentals, config.WSE_FUNDAMENTALS_STAGING_FILE)
    logger.info(f'Monthly job completed: {len(fundamentals)} wse fundamentals data fetched and saved to {config.WSE_FUNDAMENTALS_STAGING_FILE}.')
