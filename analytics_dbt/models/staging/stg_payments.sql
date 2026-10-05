-- Staging view: Standardizing payment events & normalizing currencies
WITH source AS (
    SELECT * FROM fintech_raw.payments
)
SELECT 
    transaction_id,
    idempotency_key,
    cast(timestamp as TIMESTAMP) as transaction_timestamp,
    account_id,
    merchant_id,
    card_brand,
    card_bin,
    card_last4,
    cast(amount as DECIMAL(12,2)) as amount,
    upper(currency) as currency,
    upper(status) as status,
    country_code,
    risk_score,
    cast(aml_risk_score as INTEGER) as aml_risk_score,
    is_aml_flagged,
    aml_reasons,
    ip_address
FROM source
