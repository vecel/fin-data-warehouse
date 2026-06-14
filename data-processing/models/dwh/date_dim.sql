{{ config(
    unique_key='date_id',
    materialized='incremental'
) }}

WITH date_spine AS (
    SELECT generate_series(
        '1945-01-01'::DATE, 
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

calculated_attributes AS (
    SELECT 
        TO_CHAR(calendar_date, 'YYYYMMDD')::INT AS date_id,
        calendar_date AS date,
        EXTRACT(YEAR FROM calendar_date)::INT AS year_number,
        EXTRACT(QUARTER FROM calendar_date)::INT AS quarter_number,
        TRIM(TO_CHAR(calendar_date, 'Month'))::VARCHAR(50) AS month_name,
        EXTRACT(MONTH FROM calendar_date)::INT AS month_number,
        TRIM(TO_CHAR(calendar_date, 'Day'))::VARCHAR(50) AS day_name,
        EXTRACT(ISODOW FROM calendar_date)::INT AS day_of_week_number,
        EXTRACT(DAY FROM calendar_date)::INT AS day_of_month_number,
        EXTRACT(DOY FROM calendar_date)::INT AS day_of_year_number,
        CASE 
            WHEN EXTRACT(ISODOW FROM calendar_date) IN (6, 7) THEN TRUE 
            ELSE FALSE 
        END AS is_weekend_flag
    FROM combined_date_spine
),

trading_calendars AS (
    SELECT 
        TO_CHAR(date, 'YYYYMMDD')::INT AS date_id,
        is_us_trading_day AS is_united_states_trading_day_flag,
        is_pl_trading_day AS is_poland_trading_day_flag,
        is_us_early_close AS is_united_states_early_close_day_flag
    FROM raw.calendars
),

date_dim AS (
    SELECT 
        ca.*,
        tc.is_united_states_trading_day_flag,
        tc.is_united_states_early_close_day_flag,
        tc.is_poland_trading_day_flag
    FROM calculated_attributes ca
    LEFT JOIN trading_calendars tc
    ON ca.date_id = tc.date_id
)

SELECT * FROM date_dim
{% if is_incremental() %}
  WHERE date_id NOT IN (SELECT date_id FROM {{ this }})
{% endif %}