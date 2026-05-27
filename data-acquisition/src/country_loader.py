import pandas as pd
import pycountry

def get_countries():
    country_data = [
        {'name': country.name, 'code': country.alpha_2} 
        for country in pycountry.countries
    ]
    countries_df = pd.DataFrame(country_data)
    countries_df.loc[countries_df['code'] == 'CZ', 'name'] = 'Czech Republic'
    return countries_df