{{ config(
    unique_key='indicator_id',
    materialized='incremental',
    incremental_strategy='merge',
    on_schema_change='sync_all_columns'
) }}

WITH indicators AS (
    SELECT DISTINCT
        indicator_code::VARCHAR(20) AS indicator_code,
        indicator_name::VARCHAR(100) AS indicator_name,
        'Monthly/Quarterly'::VARCHAR(20) AS frequency
    FROM raw.macro
),

macro_indicator_dim AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['indicator_code']) }} AS indicator_id,
        indicator_code,
        indicator_name,
        frequency
    FROM indicators
)

SELECT * FROM macro_indicator_dim