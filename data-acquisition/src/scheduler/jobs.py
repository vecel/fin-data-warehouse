from src.fetchers.calendars import fetch_trading_calendars
from src.writer.parquet_writer import writer
from config import config

def bootstrap_job():
    pass

def calendars_annual_job():
    calendars = fetch_trading_calendars()
    writer.write(calendars, config.CALENDARS_STAGING_FILE)
