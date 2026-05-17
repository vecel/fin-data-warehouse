import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import logging

import src.config as config

logger = logging.getLogger('ticker_loader')

def load_nasdaq_tickers() -> None:
    url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
    try:
        df = pd.read_csv(url, sep='|')
        df = df.dropna(subset=['Symbol'])
        df = df[:-1]
        df = df[~df['Security Name'].str.contains('Test')]
        tickers = df['Symbol'].astype(str).tolist()

        with open(config.NASDAQ_TICKERS_FILE, 'w') as file:
            for ticker in tickers:
                file.write(f'{ticker}\n')
    except Exception as e:
        logger.error('Nasdaq ticker loading exception. {e}')

def load_nyse_tickers() -> list:
    url = "ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt"
    try:
        df = pd.read_csv(url, sep='|')
        df = df.dropna(subset=['ACT Symbol'])
        df = df[df['Exchange'] == 'N']
        df = df[~df['ACT Symbol'].str.contains(r'\$|\.')]
        return df['ACT Symbol'].astype(str).tolist()
    except Exception as e:
        return []

def load_wse_tickers() -> list:
    url = 'https://www.biznesradar.pl/gielda/akcje_gpw'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        return []
        
    soup = BeautifulSoup(response.text, 'html.parser')
    yf_tickers = set()
    
    links = soup.find_all('a', href=re.compile(r'^/notowania/'))
    
    for link in links:
        link_text = link.get_text(strip=True)
        match = re.search(r'^(.{3})', link_text)
        
        if match:
            ticker = match.group(1).strip()
            
            if ticker.isalnum():
                yf_tickers.add(f"{ticker}.WA")
                
    return list(yf_tickers)
