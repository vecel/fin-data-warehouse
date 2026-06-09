import os

class Config:
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')

    STAGING_DIRECTORY = os.getenv('STAGING_DIRECTORY')

    STAGING_GLOBS = {
        'calendars': 'calendars.parquet',
        'countries': 'countries.parquet',
        'fundamentals': '*_fundamentals.parquet',
        'quotes': 'quotes.parquet',
        'market_news': 'news.parquet',
    }

    PRIMARY_KEYS = {
        'calendars': ['date'],
        'countries': ['code'],
        'fundamentals': ['symbol'],
        'quotes': ['ticker', 'date'],
        'market_news': ['ticker', 'source_link'],
    }

config = Config()