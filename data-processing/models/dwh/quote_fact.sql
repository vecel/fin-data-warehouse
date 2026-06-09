{{ config(
    materialized='table'
) }}

WITH quotes AS (
    SELECT
        ticker AS instrument_code,
        date AS quote_date,
        open_price,
        high_price,
        low_price,
        close_price,
        volume_number
    FROM raw.quotes
),

quote_fact AS (
    SELECT
        i.instrument_id,
        {{ to_date_id('q.quote_date') }} AS date_id,
q.open_price::NUMERIC::MONEY AS open_price,
        q.close_price::NUMERIC::MONEY AS close_price,
        q.low_price::NUMERIC::MONEY AS low_price,
        q.high_price::NUMERIC::MONEY AS high_price,
        q.volume_number::BIGINT AS volume_number
    FROM quotes q
    LEFT JOIN {{ ref('instrument_dim') }} i ON q.instrument_code = i.instrument_code
    WHERE i.instrument_id IS NOT NULL
)

SELECT * FROM quote_fact