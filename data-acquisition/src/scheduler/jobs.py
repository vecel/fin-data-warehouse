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
from src.fetchers.fred import fetch_macro_data
from src.fetchers.quotes import fetch_quotes
from src.fetchers.news import fetch_market_news
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
        wse_tickers = wse_tickers[~wse_tickers['ticker'].isin(wse_delisted)]
        writer.write(wse_tickers, config.WSE_TICKERS_CACHE_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(wse_tickers)} WSE tickers to {config.WSE_TICKERS_CACHE_FILE}.')

#    if not _exists(config.NASDAQ_TICKERS_CACHE_FILE):
#        nasdaq_tickers = fetch_nasdaq_tickers()
#        writer.write(nasdaq_tickers, config.NASDAQ_TICKERS_CACHE_FILE)
#        logger.info(f'Bootstrap job completed: Saved {len(nasdaq_tickers)} Nasdaq tickers to {config.NASDAQ_TICKERS_CACHE_FILE}.')

#    if not _exists(config.NYSE_TICKERS_CACHE_FILE):
#        nyse_tickers = fetch_nyse_tickers()
#        writer.write(nyse_tickers, config.NYSE_TICKERS_CACHE_FILE)
#        logger.info(f'Bootstrap job completed: Saved {len(nyse_tickers)} Nyse tickers to {config.NYSE_TICKERS_CACHE_FILE}.')
#
    if not _exists(config.WSE_FUNDAMENTALS_STAGING_FILE):
        wse_tickers_df = writer.read(config.WSE_TICKERS_CACHE_FILE)
        wse_tickers = wse_tickers_df['ticker'].tolist()
        usa_tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'NFLX', 'TSLA', 'INTC', 'CSCO',
            'JPM', 'BAC', 'V', 'MA', 'AXP', 'GS', 'MS', 'JNJ', 'PFE', 'UNH', 'PG', 'KO', 
            'PEP', 'WMT', 'MCD', 'DIS', 'BA', 'CAT', 'XOM', 'CVX']
        all_tickers = wse_tickers + usa_tickers
        all_fundamentals = fetch_fundamentals(all_tickers)
        writer.write(all_fundamentals, config.WSE_FUNDAMENTALS_STAGING_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(all_fundamentals)} combined fundamentals.')

    # CBX not found
    # if not _exists(config.NYSE_FUNDAMENTALS_STAGING_FILE):
    #     fundamentals = _fetch_fundamentals(config.NYSE_TICKERS_CACHE_FILE)
    #     writer.write(fundamentals, config.NYSE_FUNDAMENTALS_STAGING_FILE)
    #     logger.info(f'Bootstrap job completed: Saved {len(fundamentals)} fundamentals to {config.NYSE_FUNDAMENTALS_STAGING_FILE}.')

    if not _exists(config.MACRO_STAGING_FILE):
        macro_data = fetch_macro_data()
        writer.write(macro_data, config.MACRO_STAGING_FILE)
        logger.info(f'Bootstrap job completed: Saved {len(macro_data)} macro records to {config.MACRO_STAGING_FILE}.')

    if not _exists(config.QUOTES_STAGING_FILE):
        quotes_data = quotes_daily_job()
        logger.info(f'Bootstrap job completed: Saved {len(quotes_data)} quotes records to {config.QUOTES_STAGING_FILE}.')

    if not _exists(config.NEWS_STAGING_FILE):
        try:
            news_data = fetch_market_news(limit=200)
            writer.write(news_data, config.NEWS_STAGING_FILE)
            logger.info(f'Bootstrap job completed: Saved {len(news_data)} news recodrs to {config.NEWS_STAGING_FILE}.')
        except Exception as e:
            logger.error(f'Bootstrap job error: Cannot save market news. Exception: {e}')

def calendars_annual_job():
    calendars = fetch_trading_calendars()
    writer.write(calendars, config.CALENDARS_STAGING_FILE)
    logger.info(f'Annual job completed: {len(calendars)} calendars data fetched and saved to {config.CALENDARS_STAGING_FILE}.')


def wse_fundamentals_monthly_job():
    fundamentals = _fetch_fundamentals(config.WSE_TICKERS_CACHE_FILE)
    writer.write(fundamentals, config.WSE_FUNDAMENTALS_STAGING_FILE)
    logger.info(f'Monthly job completed: {len(fundamentals)} wse fundamentals data fetched and saved to {config.WSE_FUNDAMENTALS_STAGING_FILE}.')

def macro_monthly_job():
    macro = fetch_macro_data()
    writer.write(macro, config.MACRO_STAGING_FILE)
    logger.info(f'Monthly job completed: {len(macro)} macro data fetched and saved to {config.MACRO_STAGING_FILE}.')

def quotes_daily_job():
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'NFLX', 'TSLA', 'INTC', 'CSCO',
        'JPM', 'BAC', 'V', 'MA', 'AXP', 'GS', 'MS',
        'JNJ', 'PFE', 'UNH', 'PG', 'KO', 'PEP', 'WMT', 'MCD', 'DIS', 'BA', 'CAT', 'XOM', 'CVX',
        'PKO.WA', 'PEO.WA', 'PZU.WA', 'PKN.WA', 'DNP.WA', 'ALE.WA', 'CDR.WA', 
        'KGH.WA', 'LPP.WA', 'SPL.WA', 'KRU.WA', 'MBK.WA', 'ALR.WA', 'BHW.WA', 
        'CPS.WA', 'KTY.WA', 'MIL.WA', 'TPE.WA', 'ACP.WA', 'EAT.WA']
    
    quotes = fetch_quotes(tickers, period='5y')
    #wse_df = writer.read(config.WSE_TICKERS_CACHE_FILE)
    #nasdaq_df = writer.read(config.NASDAQ_TICKERS_CACHE_FILE)
    #tickers = wse_df['ticker'].tolist() + nasdaq_df['ticker'].tolist()
    # 500 tickers for testing
    #quotes = fetch_quotes(tickers[:500], period='5d') 
    writer.write(quotes, config.QUOTES_STAGING_FILE)
    logger.info(f'Daily job completed: {len(quotes)} quote data fetched and saved to {config.QUOTES_STAGING_FILE}.')
    return quotes

def news_daily_job():
    usa_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META']
    news = fetch_market_news(tickers=usa_tickers, limit=200)
    writer.write(news, config.NEWS_STAGING_FILE)
    logger.info(f'Daily job completed: {len(news)} news data fetched and saved to {config.NEWS_STAGING_FILE}.')