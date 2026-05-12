import pandas as pd

def load_nasdaq_tickers():
    url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
    try:
        data_frame = pd.read_csv(url, sep='|')
        data_frame = data_frame[:-1]
        data_frame = data_frame[~data_frame['Security Name'].str.contains('Test', case=False, na=False)]
        tickers = data_frame['Symbol'].dropna().astype(str).tolist()
        return tickers
    except Exception:
        return []