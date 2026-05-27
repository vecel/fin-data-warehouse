import pandas as pd
import pycountry

def get_countries():
    country_data = [
        {'name': country.name, 'code': country.alpha_2} 
        for country in pycountry.countries
    ]
    return pd.DataFrame(country_data)