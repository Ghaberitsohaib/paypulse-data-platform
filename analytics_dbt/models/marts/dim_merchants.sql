-- Dimension Table: Merchant profiles & risk classification
WITH merchants AS (
    SELECT * FROM {{ ref('stg_merchants') }}
),
tx_stats AS (
    SELECT 
        merchant_id,
        count(*) as total_transactions,
        sum(case when status = 'APPROVED' then amount else 0 end) as lifetime_volume,
        sum(case when is_aml_flagged then 1 else 0 end) as total_aml_flags
    FROM {{ ref('stg_payments') }}
    GROUP BY merchant_id
)
SELECT 
    m.merchant_id,
    m.legal_name,
    m.mcc_code,
    m.category_name,
    m.country_code,
    m.interchange_rate,
    m.reserve_holdback_rate,
    m.payout_schedule,
    m.kyc_verified,
    coalesce(t.total_transactions, 0) as total_transactions,
    coalesce(t.lifetime_volume, 0.0) as lifetime_volume,
    coalesce(t.total_aml_flags, 0) as total_aml_flags,
    CASE 
        WHEN coalesce(t.total_aml_flags, 0) > 3 THEN 'HIGH_RISK_TIER'
        WHEN coalesce(t.lifetime_volume, 0) > 10000 THEN 'VIP_PARTNER'
        ELSE 'STANDARD_TIER'
    END as merchant_risk_tier
FROM merchants m
LEFT JOIN tx_stats t ON m.merchant_id = t.merchant_id
