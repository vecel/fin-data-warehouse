SELECT d.instrument_code, SUM(high_price), SUM(low_price), SUM(open_price), SUM(close_price), AVG(volume_number), AVG(instrument_sentiment_value), AVG(instrument_relevance_value), AVG(aggregated_news_sentiment_value)
FROM dwh.instrument_dim d 
LEFT JOIN dwh.quote_fact f ON f.instrument_id = d.instrument_id
LEFT JOIN dwh.market_news_fact n ON d.instrument_id = n.instrument_id
GROUP BY d.instrument_code, d.instrument_quote_type_name