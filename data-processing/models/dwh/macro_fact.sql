{{ config(
    unique_key='macro_fact_id',
    materialized='incremental'
) }}

WITH macro_raw AS (
    SELECT
        date AS macro_date,
        indicator_value,
        indicator_code,
        country_code
    FROM raw.macro
),

macro_fact AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['m.indicator_code', 'm.macro_date', 'm.country_code']) }} AS macro_fact_id,
        {{ to_date_id('m.macro_date') }} AS date_id,
        c.country_id,
        i.indicator_id,
        m.indicator_value::DOUBLE PRECISION AS indicator_value
    FROM macro_raw m
    LEFT JOIN {{ ref('country_dim') }} c ON m.country_code = c.country_code
    LEFT JOIN {{ ref('macro_indicator_dim') }} i ON m.indicator_code = i.indicator_code
    WHERE c.country_id IS NOT NULL AND i.indicator_id IS NOT NULL
)

SELECT * FROM macro_fact
{% if is_incremental() %}
  WHERE macro_fact_id NOT IN (SELECT macro_fact_id FROM {{ this }})
{% endif %}