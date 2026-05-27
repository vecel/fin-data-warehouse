WITH raw_seed AS (
    SELECT * FROM {{ ref('trading_calendars') }}
),

transformed AS (
    SELECT 
        CAST(date AS DATE) AS calendar_date,
        CAST(is_us_trading_day AS BOOLEAN) AS is_united_states_trading_day_flag,
        CAST(is_us_early_close AS BOOLEAN) AS is_united_states_early_close_day_flag,
        CAST(is_pl_trading_day AS BOOLEAN) AS is_poland_trading_day_flag

    FROM raw_seed
)

SELECT 
    TO_CHAR(calendar_date, 'YYYYMMDD')::INT AS date_id,
    is_united_states_trading_day_flag,
    is_poland_trading_day_flag,
    is_united_states_early_close_day_flag
FROM transformed