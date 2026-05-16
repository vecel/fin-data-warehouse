import pandas as pd
from fredapi import Fred

# Indexes to gather
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

def load_fred_data(api_key: str) -> pd.DataFrame:
    fred = Fred(api_key=api_key)
    all_data = []

    for name, code in FRED_SERIES_MAP.items():
        try:
            series = fred.get_series(code)
            df = series.reset_index()
            df.columns = ['date', 'indicator_value']
            df['indicator_code'] = code
            df['indicator_name_custom'] = name
            
            all_data.append(df)
        except Exception as e:
            print(f"Error loading code {code}: {e}")

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.dropna(subset=['indicator_value'])
        return final_df
    
    print("No data found!")
    return pd.DataFrame()