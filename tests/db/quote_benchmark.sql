SELECT d.instrument_code, SUM(high_price) AS sum_high, AVG(volume_number) AS avg_volume
FROM dwh.instrument_dim d LEFT JOIN dwh.quote_fact f ON f.instrument_id = d.instrument_id
WHERE f.date_id > 20260608
GROUP BY d.instrument_code