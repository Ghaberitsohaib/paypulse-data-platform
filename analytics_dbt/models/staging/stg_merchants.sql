-- Staging view: Merchant business catalog & KYC status
WITH source AS (
    SELECT * FROM fintech_raw.merchants
)
SELECT 
    merchant_id,
    legal_name,
    mcc_code,
    category_name,
    country_code,
    cast(interchange_rate as DECIMAL(6,4)) as interchange_rate,
    cast(reserve_holdback_rate as DECIMAL(6,4)) as reserve_holdback_rate,
    payout_schedule,
    kyc_verified,
    cast(registered_at as TIMESTAMP) as registered_at
FROM source
