import logging
import pandas as pd
import yfinance as yf

logger = logging.getLogger('quote_loader')

# TODO: Add appending to file or separete files for info. Currently overriding last tickers info file.
# TODO: Add cache for tickers info as they do not need to be fetched every time.
def fetch_tickers_info(tickers):
    logger.info(f'Fetching tickers info for {len(tickers)} tickers.')
    tickers_str = ' '.join(tickers)
    tickers = yf.Tickers(tickers_str)
    infos = [ticker.info for _, ticker in tickers.tickers.items()]
    logger.info(f'Successfully fetched {len(infos)} tickers info.')
    return pd.DataFrame(infos)
