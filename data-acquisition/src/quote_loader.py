import logging
import pandas as pd
import yfinance as yf

from src.ticker_loader import read_all_tickers

logger = logging.getLogger('quote_loader')

def fetch_instrument_data(save_path):
    logger.info('Fetching instrument data.')
    tickers = read_all_tickers()
    logger.info(f'Loaded {len(tickers)} tickers. Starting download instrument data.')

    batch = " ".join(tickers[:20])
    t = yf.Tickers(batch)
    infos = [ticker.info for _, ticker in t.tickers.items()]
    df = pd.DataFrame(infos)
    df.to_csv(save_path, index=False)
