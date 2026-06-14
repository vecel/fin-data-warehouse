{{ config(
    unique_key='market_news_id'
) }}

WITH news AS (
    SELECT
        ticker AS instrument_code,
        news_title_name,
        source_name,
        source_link,
        SUBSTRING(published_at, 1, 8) AS published_date_str,
        aggregated_news_sentiment_score,
        aggregated_news_sentiment_label,
        news_primary_topic_name,
        news_primary_topic_relevance_value,
        {{ null_if_on_string("news_secondary_topic_name", "news_secondary_topic_name") }},
        news_secondary_topic_relevance_value,
        {{ null_if_on_string("news_tertiary_topic_name", "news_tertiary_topic_name") }},
        news_tertiary_topic_relevance_value,
        instrument_relevance_value,
        instrument_sentiment_value,
        instrument_sentiment_name
    FROM raw.market_news
),

market_news_fact AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['n.source_link', 'n.instrument_code']) }} AS market_news_id,
        i.instrument_id,
        n.published_date_str::BIGINT AS date_id,
        n.news_title_name::VARCHAR(250),
        n.instrument_relevance_value::DOUBLE PRECISION,
        n.instrument_sentiment_value::DOUBLE PRECISION,
        n.instrument_sentiment_name::VARCHAR(50),
        n.aggregated_news_sentiment_score::DOUBLE PRECISION AS aggregated_news_sentiment_value,
        n.aggregated_news_sentiment_label::VARCHAR(50) AS aggregated_news_sentiment_name,
        n.news_primary_topic_name::VARCHAR(50),
        n.news_primary_topic_relevance_value::DOUBLE PRECISION,
        COALESCE(n.news_secondary_topic_name::VARCHAR(50), 'Not aplicable') AS news_secondary_topic_name,
        COALESCE(n.news_secondary_topic_relevance_value::DOUBLE PRECISION, -1) AS news_secondary_topic_relevance,
        COALESCE(n.news_tertiary_topic_name::VARCHAR(50), 'Not aplicable') AS news_tertiary_topic_name,
        COALESCE(n.news_tertiary_topic_relevance_value::DOUBLE PRECISION, -1) AS news_tertiary_topic_relevance,
        n.source_name::VARCHAR(50),
        'General'::VARCHAR(50) AS news_category_within_source_name,
        n.source_link::VARCHAR(200)
    FROM news n
    LEFT JOIN {{ ref('instrument_dim') }} i ON n.instrument_code = i.instrument_code
    WHERE i.instrument_id IS NOT NULL
)

SELECT * FROM market_news_fact