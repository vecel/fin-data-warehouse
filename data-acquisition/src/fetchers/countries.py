import logging
import pandas as pd
import pycountry

logger = logging.getLogger(__name__)

def fetch_countries():
    logger.info('Fetching country codes')
    country_data = [
        {'name': country.name, 'code': country.alpha_2} 
        for country in pycountry.countries
    ]
    countries_df = pd.DataFrame(country_data)
    countries_df.loc[countries_df['code'] == 'CZ', 'name'] = 'Czech Republic'
    countries_df.loc[countries_df['code'] == 'KR', 'name'] = 'South Korea'
    countries_df.loc[countries_df['code'] == 'TR', 'name'] = 'Turkey'
    countries_df.loc[countries_df['code'] == 'TW', 'name'] = 'Taiwan'
    return countries_df