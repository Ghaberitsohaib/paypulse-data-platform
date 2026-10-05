-- Staging view: Currency FX reference conversion
WITH source AS (
    SELECT * FROM fintech_raw.fx_rates
)
SELECT 
    base_currency,
    target_currency,
    cast(exchange_rate as DECIMAL(10,4)) as exchange_rate,
    cast(rate_date as DATE) as rate_date
FROM source
