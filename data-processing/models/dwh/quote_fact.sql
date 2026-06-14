{{ config(
    unique_key=['instrument_id', 'date_id'],
    materialized='incremental',
    incremental_strategy='merge',
    on_schema_change='sync_all_columns'
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

source AS (
    SELECT DISTINCT
        symbol AS instrument_code,
        exchange,
        {{ null_if_on_string('country', 'country') }}
    FROM raw.fundamentals
),

instrument_info AS (
    SELECT DISTINCT
        instrument_code,
        exchange,
        COALESCE(country, 'Unavailable') AS country
    FROM source
),

quote_fact AS (
    SELECT
        i.instrument_id,
        {{ to_date_id('q.quote_date') }} AS date_id,
        e.exchange_id,
        c.country_id,
        q.open_price::NUMERIC::MONEY AS open_price,
        q.close_price::NUMERIC::MONEY AS close_price,
        q.low_price::NUMERIC::MONEY AS low_price,
        q.high_price::NUMERIC::MONEY AS high_price,
        q.volume_number::BIGINT AS volume_number
    FROM quotes q
    LEFT JOIN {{ ref('instrument_dim') }} i ON q.instrument_code = i.instrument_code
    LEFT JOIN instrument_info ii ON q.instrument_code = ii.instrument_code
    LEFT JOIN {{ ref('exchange_dim') }} e ON ii.exchange = e.exchange_code
    LEFT JOIN {{ ref('country_dim') }} c ON ii.country = c.country_name
    WHERE i.instrument_id IS NOT NULL
)

SELECT * FROM quote_fact