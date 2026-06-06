{% snapshot instrument_dim_snapshot %}

{{
    config(
        unique_key='instrument_id',
        strategy='check',
        check_cols=[
            'instrument_price_category',
            'yearly_price_change_category',
            'last_dividend_date_id',
            'last_dividend_yield_category'
        ],
        invalidate_hard_deletes=True
    )
}}

WITH renamed AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['symbol']) }} AS instrument_id,
        "currentPrice"::FLOAT AS current_price,
        "fiftyTwoWeekChangePercent"::FLOAT AS fifty_two_week_change_percent,
        TO_CHAR(
            (TO_TIMESTAMP("lastDividendDate"::FLOAT)
            AT TIME ZONE 'UTC')::DATE,
            'YYYYMMDD')::INT AS last_dividend_date_id,
        "dividendYield"::FLOAT AS last_dividend_yield
    FROM raw.fundamentals
),

calculated AS (
    SELECT 
        instrument_id,
        (CASE
            WHEN current_price < 5 THEN 'Penny Stock'
            WHEN current_price < 25 THEN 'Low Stock'
            WHEN current_price < 100 THEN 'Mid Stock'
            ELSE 'High Stock'
        END)::VARCHAR(50) AS instrument_price_category,
        (CASE
            WHEN fifty_two_week_change_percent < -50 THEN 'High Loss'
            WHEN fifty_two_week_change_percent < -20 THEN 'Moderate Loss'
            WHEN fifty_two_week_change_percent < -5 THEN 'Low Loss'
            WHEN fifty_two_week_change_percent < 5 THEN 'Neutral'
            WHEN fifty_two_week_change_percent < 20 THEN 'Low Gain'
            WHEN fifty_two_week_change_percent < 50 THEN 'Moderate Gain'
            ELSE 'High Gain'
        END)::VARCHAR(50) AS yearly_price_change_category,
        COALESCE(last_dividend_date_id, 99991231) AS last_dividend_date_id,
        (CASE
            WHEN last_dividend_yield IS NULL THEN 'Unavailable'
            WHEN last_dividend_yield < 2 THEN 'Low Dividend Yield'
            WHEN last_dividend_yield < 10 THEN 'Moderate Dividend Yield'
            ELSE 'High Dividend Yield'
        END)::VARCHAR(50) AS last_dividend_yield_category
    FROM renamed
)

SELECT
    instrument_id,
    instrument_price_category,
    yearly_price_change_category,
    last_dividend_date_id,
    last_dividend_yield_category
FROM calculated

{% endsnapshot %}