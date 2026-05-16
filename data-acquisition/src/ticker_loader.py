import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def load_nasdaq_tickers() -> pd.DataFrame:
    url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
    try:
        data_frame = pd.read_csv(url, sep='|')
        data_frame = data_frame[:-1]
        data_frame = data_frame[~data_frame['Security Name'].str.contains('Test', case=False, na=False)]
        tickers = data_frame['Symbol'].dropna().astype(str).tolist()
        return tickers
    except Exception:
        return []

def load_wse_tickers():
    url = 'https://www.biznesradar.pl/gielda/akcje_gpw'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"Connecting to {url}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data: {e}")
        return []
        
    soup = BeautifulSoup(response.text, 'html.parser')
    yf_tickers = set()
    
    links = soup.find_all('a', href=re.compile(r'^/notowania/'))
    
    for link in links:
        link_text = link.get_text(strip=True)
        print(link_text)
        
        match = re.search(r'^(.{3})', link_text)
        
        if match:
            ticker = match.group(1).strip()
            
            if ticker.isalnum():
                yf_tickers.add(f"{ticker}.WA")
                
    return sorted(list(yf_tickers))
