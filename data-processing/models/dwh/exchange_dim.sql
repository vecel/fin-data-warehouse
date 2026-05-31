{{ config(
    unique_key='exchange_id'
) }}

WITH exchange_dim AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['exchange']) }} AS exchange_id,
        "fullExchangeName"::VARCHAR(50) AS exchange_name,
        exchange::VARCHAR(20) AS exchange_code,
        "exchangeTimezoneName"::VARCHAR(50) AS exchange_timezone_name,
        "exchangeTimezoneShortName"::VARCHAR(20) AS exchange_timezone_code,
        currency::VARCHAR(20) AS exchange_currency_code
    FROM stg.fundamentals
)

SELECT * FROM exchange_dim