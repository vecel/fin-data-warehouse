{{ config(materialized='table') }}

WITH daily_news AS (
    SELECT 
        instrument_id,
        date_id,
        COUNT(market_news_id) as news_count,
        AVG(aggregated_news_sentiment_value) as avg_daily_sentiment,
        MAX(news_title_name) as top_headline
    FROM {{ ref('market_news_fact') }}
    GROUP BY instrument_id, date_id
),

quotes AS (
    SELECT 
        instrument_id,
        date_id,
        close_price,
        volume_number
    FROM {{ ref('quote_fact') }}
)

SELECT 
    q.instrument_id,
    q.date_id,
    d.date as reporting_date,
    q.close_price,
    q.volume_number,
    COALESCE(n.news_count, 0) as news_count,
    COALESCE(n.avg_daily_sentiment, 0) as avg_daily_sentiment,
    n.top_headline
FROM quotes q
JOIN {{ ref('date_dim') }} d ON q.date_id = d.date_id
LEFT JOIN daily_news n ON q.instrument_id = n.instrument_id AND q.date_id = n.date_id
ORDER BY q.instrument_id, q.date_id DESC