-- Fact Table: Regulatory SAR (Suspicious Activity Reports) feed for Compliance Officers
SELECT 
    transaction_id,
    transaction_timestamp,
    account_id,
    merchant_id,
    merchant_name,
    card_brand,
    original_amount,
    currency,
    amount_usd,
    country_code,
    aml_risk_score,
    aml_reasons
FROM {{ ref('fct_transactions') }}
WHERE is_aml_flagged = true OR aml_risk_score >= 70
ORDER BY aml_risk_score DESC
