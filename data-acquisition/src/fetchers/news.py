import os
import requests
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def fetch_market_news(tickers=None, limit=50):
    logger.info('Fetching market news and sentiment.')
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        logger.error('Missing ALPHA_VANTAGE_API_KEY environment variable!')
        return pd.DataFrame()

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&limit={limit}&apikey={api_key}"
    if tickers:
        tickers_str = ",".join(tickers[:30]) 
        url += f"&tickers={tickers_str}"
        
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'feed' not in data:
            logger.warning("No 'feed' data returned from Alpha Vantage. Rate limit exceeded?")
            return pd.DataFrame()

        news_list = []
        for item in data['feed']:
            base_info = {
                'news_title_name': item.get('title'),
                'source_name': item.get('source'),
                'source_link': item.get('url'),
                'published_at': item.get('time_published'),
                'aggregated_news_sentiment_score': float(item.get('overall_sentiment_score', 0)),
                'aggregated_news_sentiment_label': item.get('overall_sentiment_label')
            }
            
            topics = item.get('topics', [])
            for i, topic in enumerate(topics[:3]):
                prefix = ['primary', 'secondary', 'tertiary'][i]
                base_info[f'news_{prefix}_topic_name'] = topic.get('topic')
                base_info[f'news_{prefix}_topic_relevance_value'] = float(topic.get('relevance_score', 0))

            ticker_sentiments = item.get('ticker_sentiment', [])
            if ticker_sentiments:
                for ts in ticker_sentiments:
                    row = base_info.copy()
                    row['ticker'] = ts.get('ticker')
                    row['instrument_relevance_value'] = float(ts.get('relevance_score', 0))
                    row['instrument_sentiment_value'] = float(ts.get('ticker_sentiment_score', 0))
                    row['instrument_sentiment_name'] = ts.get('ticker_sentiment_label')
                    news_list.append(row)
            else:
                base_info['ticker'] = 'UNKNOWN'
                news_list.append(base_info)

        return pd.DataFrame(news_list)

    except Exception as e:
        logger.error(f'Error fetching news data: {e}')
        return pd.DataFrame()