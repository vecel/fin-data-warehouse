{{ config(
    unique_key='country_id'
) }}

WITH codes AS (
    SELECT DISTINCT
        name::VARCHAR(50) AS country_name,
        code::VARCHAR(20) AS country_code
    FROM stg.countries
),

names AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['country']) }} AS country_id,
        country::VARCHAR(50) AS country_name
    FROM stg.fundamentals
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