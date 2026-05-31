import time
import logging
import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

CHUNK_SIZE = 100
PAUSE_PER_CHUNK = 1

def _chunked(array, chunk_size):
    for i in range(0, len(array), chunk_size):
        yield array[i:i + chunk_size]

def fetch_fundamentals(tickers):
    logger.info(f'Fetching fundamentals data for {len(tickers)} tickers')

    chunks = list(_chunked(tickers, CHUNK_SIZE))
    chunks_num = len(chunks)

    infos = []
    for idx, chunk in enumerate(chunks):
        logger.debug(f'Fetching chunk {idx + 1}/{chunks_num}')
        chunk_tickers_str = ' '.join(chunk)
        chunk_tickers = yf.Tickers(chunk_tickers_str)
        chunk_infos = [ticker.info for _, ticker in chunk_tickers.tickers.items()]
        infos.extend(chunk_infos)
        time.sleep(PAUSE_PER_CHUNK)

    return pd.DataFrame(infos, dtype=str)
