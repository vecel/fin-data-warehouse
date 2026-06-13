{{ config(
    materialized='table'
) }}

WITH quotes AS (
    SELECT 
        q.instrument_id,
        q.date_id,
        q.country_id,
        q.close_price,
        d.year_number,
        d.month_number,
        d.date AS quote_date
    FROM {{ ref('quote_fact') }} q
    JOIN {{ ref('date_dim') }} d ON q.date_id = d.date_id
),

inflation AS (
    SELECT 
        m.country_id,
        d.year_number,
        d.month_number,
        m.indicator_value AS cpi_value
    FROM {{ ref('macro_fact') }} m
    JOIN {{ ref('macro_indicator_dim') }} ind ON m.indicator_id = ind.indicator_id
    JOIN {{ ref('date_dim') }} d ON m.date_id = d.date_id
    WHERE ind.indicator_code IN ('CPIAUCSL', 'POLCPIALLMINMEI')
),


joined_data AS (
    SELECT 
        q.instrument_id,
        q.date_id,
        q.quote_date,
        q.close_price,
        i.cpi_value
    FROM quotes q
    LEFT JOIN inflation i 
        ON q.country_id = i.country_id 
        AND q.year_number = i.year_number 
        AND q.month_number = i.month_number
),

base_cpi_calc AS (
    SELECT 
        instrument_id,
        FIRST_VALUE(cpi_value) OVER (
            PARTITION BY instrument_id 
            ORDER BY quote_date ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS base_cpi
    FROM joined_data
    WHERE cpi_value IS NOT NULL
)

SELECT 
    j.instrument_id,
    j.date_id,
    j.quote_date,
    j.close_price AS nominal_close_price,
    j.cpi_value AS current_cpi,
    b.base_cpi,
    (j.close_price::NUMERIC * (b.base_cpi / j.cpi_value))::NUMERIC::MONEY AS real_close_price
FROM joined_data j
JOIN (
    SELECT DISTINCT instrument_id, base_cpi FROM base_cpi_calc
) b ON j.instrument_id = b.instrument_id
WHERE j.cpi_value IS NOT NULL
ORDER BY j.instrument_id, j.quote_date DESC