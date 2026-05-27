{{ config(
    unique_key='country_id'
) }}

WITH codes AS (
    SELECT DISTINCT
        country_name,
        country_code
    FROM {{ ref('countries_stg') }}
),

names AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['country_name']) }} AS country_id,
        country_name
    FROM {{ ref('tickers_info_stg') }}
),

country_dim AS (
    SELECT
        cn.*,
        CASE
            WHEN cn.country_name = 'Unknown' THEN 'Unavailable'
            ELSE cc.country_code
        END
    FROM names cn
    LEFT JOIN codes cc
    ON cn.country_name = cc.country_name
)

SELECT * FROM country_dim