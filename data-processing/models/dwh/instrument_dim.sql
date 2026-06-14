{{ config(
    unique_key='instrument_id'
) }}

WITH renamed AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['symbol']) }} AS instrument_id,
        symbol::VARCHAR(20) AS instrument_code,
        NULLIF(NULLIF(TRIM("shortName"::VARCHAR(50)), ''), 'null') AS instrument_short_name,
        NULLIF(NULLIF(TRIM("longName"::VARCHAR(50)), ''), 'null') AS instrument_long_name,
        city::VARCHAR(50) AS city_name,
        state::VARCHAR(50) AS state_name,
        zip::VARCHAR(20) AS zip_code,
        CASE 
            WHEN market = 'pl_market' THEN 'Poland'
            WHEN market = 'us_market' THEN 'USA'
            ELSE market
        END::VARCHAR(50) AS instrument_market_name,
        "quoteType"::VARCHAR(50) AS instrument_quote_type_name,
        NULLIF(NULLIF(TRIM(sector::VARCHAR(50)), ''), 'null') AS instrument_sector_name,
        NULLIF(NULLIF(TRIM(industry::VARCHAR(50)), ''), 'null') AS instrument_industry_name,
        "currentPrice"::FLOAT AS current_price,
        "fiftyTwoWeekChangePercent"::FLOAT AS fifty_two_week_change_percent,
        TO_CHAR(
            (TO_TIMESTAMP(NULLIF("lastDividendDate", 'nan')::FLOAT)
            AT TIME ZONE 'UTC')::DATE,
            'YYYYMMDD')::INT AS last_dividend_date_id,
        "dividendYield"::FLOAT AS last_dividend_yield
    FROM raw.fundamentals
),

instrument_dim AS (
    SELECT 
        {{ dbt_utils.generate_surrogate_key(['snap.instrument_id', 'snap.dbt_valid_from']) }} AS instrument_id,
        curr.instrument_code,
        COALESCE(curr.instrument_short_name, curr.instrument_long_name, 'Not Aplicable') AS instrument_short_name,
        COALESCE(curr.instrument_long_name, curr.instrument_short_name, 'Not Aplicable') AS instrument_long_name,
        COALESCE(curr.city_name, 'Not Aplicable') AS city_name,
        COALESCE(curr.state_name, curr.city_name, 'Not Aplicable') AS state_name,
        COALESCE(curr.zip_code, 'Not Aplicable') AS zip_code,
        COALESCE(curr.instrument_market_name, 'Unavailable') AS instrument_market_name,
        curr.instrument_quote_type_name,
        COALESCE(curr.instrument_sector_name, 'Unavailable') AS instrument_sector_name,
        COALESCE(curr.instrument_industry_name, 'Unavailable') AS instrument_industry_name,
        snap.instrument_price_category,
        snap.yearly_price_change_category,
        snap.last_dividend_date_id,
        snap.last_dividend_yield_category,
        {{ to_date_id('snap.dbt_valid_from') }} AS valid_from_date_id,
        COALESCE({{ to_date_id('snap.dbt_valid_to') }}, 99991231) AS valid_to_date_id,
        CASE 
            WHEN snap.dbt_valid_to IS NULL THEN 'YES'
            ELSE 'No'
        END AS is_active_flag
    FROM {{ ref('instrument_dim_snapshot') }} snap
    LEFT JOIN renamed curr
    ON snap.instrument_id = curr.instrument_id
)

SELECT * FROM instrument_dim