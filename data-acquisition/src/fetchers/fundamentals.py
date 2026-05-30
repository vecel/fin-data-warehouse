import logging
import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

def fetch_fundamentals(tickers):
    logger.info(f'Fetching fundamentals data for {len(tickers)} tickers.')
    tickers_str = ' '.join(tickers)
    tickers = yf.Tickers(tickers_str)
    infos = [ticker.info for _, ticker in tickers.tickers.items()]
    return pd.DataFrame(infos)
