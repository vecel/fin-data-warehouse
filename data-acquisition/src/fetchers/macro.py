import os
import logging
import pandas as pd
from fredapi import Fred

# TODO: Move to fetchers, add job, schedule job, load .env from project root

logger = logging.getLogger(__name__)

FRED_SERIES_MAP = {
    'US_GDP': 'GDP',
    'PL_GDP': 'CPMNACSCAB1GQPL',
    'US_UNRATE': 'UNRATE',
    'PL_UNRATE': 'LRHUTTTTPLM156S',
    'US_INFLATION': 'CPIAUCSL',
    'PL_INFLATION': 'POLCPIALLMINMEI',
    'US_INTEREST': 'FEDFUNDS',
    'PL_INTEREST': 'IR3TIB01PLM156N'
}

def fetch_macro_data() -> pd.DataFrame:
    logger.info('Fetching macro data from FRED.')
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        logger.error("Missing FRED_API_KEY environment variable!")
        raise ValueError("Missing FRED_API_KEY")

    fred = Fred(api_key=api_key)
    all_data = []

    for name, code in FRED_SERIES_MAP.items():
        try:
            series = fred.get_series(code)
            df = series.reset_index()
            df.columns = ['date', 'indicator_value']
            df['indicator_code'] = code
            df['indicator_name'] = name
            df['country_code'] = 'PL' if name.startswith('PL') else 'US'
            
            all_data.append(df)
        except Exception as e:
            logger.error(f"Error loading code {code}: {e}")

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.dropna(subset=['indicator_value'])
        return final_df
    
    logger.warning("No macro data found!")
    return pd.DataFrame()