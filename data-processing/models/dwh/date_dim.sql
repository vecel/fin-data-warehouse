{{ config(
    materialized='table',
    unique_key='date_id'
) }}

WITH date_spine AS (
    SELECT generate_series(
        '2020-01-01'::DATE, 
        '2030-12-31'::DATE, 
        '1 day'::INTERVAL
    )::DATE AS calendar_date
),

end_of_the_world AS (
    SELECT '9999-12-31'::DATE AS calendar_date
),

combined_date_spine AS (
    SELECT calendar_date FROM date_spine
    UNION ALL
    SELECT calendar_date FROM end_of_the_world
),

date_dim AS (
    SELECT 
        TO_CHAR(calendar_date, 'YYYYMMDD')::INT AS date_id,
        calendar_date AS date,
        EXTRACT(YEAR FROM calendar_date)::INT AS year_number,
        EXTRACT(QUARTER FROM calendar_date)::INT AS quarter_number,
        TRIM(TO_CHAR(calendar_date, 'Month')) AS month_name,
        EXTRACT(MONTH FROM calendar_date)::INT AS month_number,
        TRIM(TO_CHAR(calendar_date, 'Day')) AS day_name,
        EXTRACT(ISODOW FROM calendar_date)::INT AS day_of_week_number,
        EXTRACT(DAY FROM calendar_date)::INT AS day_of_month_number,
        EXTRACT(DOY FROM calendar_date)::INT AS day_of_year_number,
        CASE 
            WHEN EXTRACT(ISODOW FROM calendar_date) IN (6, 7) THEN TRUE 
            ELSE FALSE 
        END AS is_weekend_flag
        -- TODO: Add three trading day flags (use python script for that)
    FROM combined_date_spine
)

SELECT * FROM date_dim