{{ config(
    unique_key='instrument_id'
) }}

WITH renamed AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['symbol']) }} AS instrument_id,
        symbol::VARCHAR(20) AS instrument_code,
        "shortName"::VARCHAR(50) AS instrument_short_name,
        "longName"::VARCHAR(50) AS instrument_long_name,
        city::VARCHAR(50) AS city_name,
        state::VARCHAR(50) AS state_name,
        zip::VARCHAR(20) AS zip_code,
        market::VARCHAR(50) AS instrument_market_name,
        "quoteType"::VARCHAR(50) AS instrument_quote_type_name,
        sector::VARCHAR(50) AS instrument_sector_name,
        industry::VARCHAR(50) AS instrument_industry_name,
        "currentPrice"::FLOAT AS current_price,
        "fiftyTwoWeekChangePercent"::FLOAT AS fifty_two_week_change_percent,
        TO_CHAR(
            (TO_TIMESTAMP("lastDividendDate"::FLOAT)
            AT TIME ZONE 'UTC')::DATE,
            'YYYYMMDD')::INT AS last_dividend_date_id,
        "dividendYield"::FLOAT AS last_dividend_yield
    FROM stg.fundamentals
),

instrument_dim AS (
    SELECT 
        instrument_id,
        instrument_code,
        instrument_short_name,
        instrument_long_name,
        COALESCE(city_name, 'Not Aplicable') AS city_name,
        COALESCE(state_name, city_name, 'Not Aplicable') AS state_name,
        COALESCE(zip_code, 'Not Aplicable') AS zip_code,
        instrument_market_name,
        instrument_quote_type_name,
        COALESCE(instrument_sector_name, 'Unavailable') AS instrument_sector_name,
        COALESCE(instrument_industry_name, 'Unavailable') AS instrument_industry_name,
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
        END)::VARCHAR(50) AS last_dividend_yield_category,
        TO_CHAR(CURRENT_DATE, 'YYYYMMDD')::INT AS valid_from_date_id,
        99991231 AS valid_to_date_id,
        'YES' AS is_active_flag
    FROM renamed
)

SELECT * FROM instrument_dim