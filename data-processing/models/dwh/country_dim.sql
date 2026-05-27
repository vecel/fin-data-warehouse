{{ config(
    unique_key='country_id'
) }}

WITH country_dim AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['country_name']) }} AS country_id,
        country_name,
        -- country_code,
    FROM {{ ref('tickers_info_stg') }}
)

SELECT * FROM country_dim