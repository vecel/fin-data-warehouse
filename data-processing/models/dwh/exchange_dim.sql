{{ config(
    unique_key='exchange_id'
) }}

WITH exchange_dim AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['exchange_code']) }} AS exchange_id,
        exchange_name,
        exchange_code,
        exchange_timezone_name,
        exchange_timezone_code
    FROM {{ ref('wse_tickers_info_stg') }}
)

SELECT * FROM exchange_dim