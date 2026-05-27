WITH source AS (
    SELECT * FROM {{ ref('countries') }}
),

transformed AS (
    SELECT 
        name AS country_name,
        code AS country_code
    FROM source
)

SELECT * FROM transformed