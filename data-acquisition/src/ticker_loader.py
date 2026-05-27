import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import logging

logger = logging.getLogger('ticker_loader')


def fetch_nasdaq_tickers():
    logger.info('Fetching Nasdaq tickers.')
    url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
    try:
        df = pd.read_csv(url, sep='|')
        df = df.dropna(subset=['Symbol'])
        df = df[:-1]
        df = df[~df['Security Name'].str.contains('Test')]
        tickers = df['Symbol'].astype(str).tolist()
        return tickers
    except Exception as e:
        logger.error(f'Nasdaq ticker loading exception. {e}')


def fetch_nyse_tickers():
    logger.info('Fetching Nyse tickers.')
    url = "ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt"
    try:
        df = pd.read_csv(url, sep='|')
        df = df.dropna(subset=['ACT Symbol'])
        df = df[df['Exchange'] == 'N']
        df = df[~df['ACT Symbol'].str.contains(r'\$|\.')]
        tickers = df['ACT Symbol'].astype(str).tolist()
        return tickers
    except Exception as e:
        logger.error(f'Nyse ticker loading exception. {e}')


def fetch_wse_tickers():
    logger.info('Fetching WSE tickers.')
    url = 'https://www.biznesradar.pl/gielda/akcje_gpw'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        logger.error(f'Cannot get WSE tickers. {e}')
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    tickers = set()
    links = soup.find_all('a', href=re.compile(r'^/notowania/'))
    for link in links:
        link_text = link.get_text(strip=True)
        match = re.search(r'^(.{3})', link_text)
        if match:
            ticker = match.group(1).strip()
            if ticker.isalnum():
                tickers.add(f"{ticker}.WA")

    return list(tickers)
    