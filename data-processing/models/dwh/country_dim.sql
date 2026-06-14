{{ config(
    unique_key='country_id',
    materialized='incremental'
) }}

WITH codes AS (
    SELECT DISTINCT
        name::VARCHAR(50) AS country_name,
        code::VARCHAR(20) AS country_code
    FROM raw.countries
),

names AS (
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['country']) }} AS country_id,
        {{ null_if_on_string('country', 'country_name') }}
    FROM raw.fundamentals
),

null_renamed AS (
    SELECT 
        country_id,
        COALESCE(country_name, 'Unavailable') AS country_name
    FROM names
),

country_dim AS (
    SELECT
        cn.*,
        CASE
            WHEN cn.country_name = 'Unavailable' THEN 'Unavailable'
            ELSE cc.country_code
        END
    FROM null_renamed cn
    LEFT JOIN codes cc
    ON cn.country_name = cc.country_name
)

SELECT * FROM country_dim
{% if is_incremental() %}
  WHERE country_id NOT IN (SELECT country_id FROM {{ this }})
{% endif %}