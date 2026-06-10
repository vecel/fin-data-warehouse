import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def fetch_quotes(tickers, period='5d'):
    logger.info(f'Fetching quotes for {len(tickers)} tickers. Period: {period}')
    
    df = yf.download(tickers, period=period, group_by='ticker', threads=True)
    
    quotes_list = []
    
    for ticker in tickers:
        if ticker in df:
            ticker_df = df[ticker].dropna(how='all').copy()
            if not ticker_df.empty:
                ticker_df = ticker_df.reset_index()
                ticker_df['ticker'] = ticker
                quotes_list.append(ticker_df)
                
    if not quotes_list:
        logger.warning('No quotes fetched.')
        return pd.DataFrame()
        
    final_df = pd.concat(quotes_list, ignore_index=True)
    
    final_df = final_df.rename(columns={
        'Date': 'date', 
        'Open': 'open_price', 
        'High': 'high_price', 
        'Low': 'low_price', 
        'Close': 'close_price', 
        'Volume': 'volume_number'
    })
    
    columns_to_keep = ['ticker', 'date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume_number']
    final_df = final_df[[col for col in columns_to_keep if col in final_df.columns]]
    
    return final_df