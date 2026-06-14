{{ config(
    unique_key='exchange_id',
    materialized='incremental',
    incremental_strategy='merge',
    on_schema_change='sync_all_columns'
) }}

WITH renamed AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['exchange']) }} AS exchange_id,
        "fullExchangeName"::VARCHAR(50) AS exchange_name,
        exchange::VARCHAR(20) AS exchange_code,
        "exchangeTimezoneName"::VARCHAR(50) AS exchange_timezone_name,
        "exchangeTimezoneShortName"::VARCHAR(20) AS exchange_timezone_code,
        currency::VARCHAR(20) AS exchange_currency_code
    FROM raw.fundamentals
),

exchange_dim AS (
    SELECT *
    FROM renamed
    WHERE exchange_name IS NOT NULL
        AND exchange_code IS NOT NULL
        AND exchange_timezone_name IS NOT NULL
        AND exchange_timezone_code IS NOT NULL
        AND exchange_currency_code IS NOT NULL
)

SELECT * 
FROM exchange_dim