-- Fact Table: Atomic reconciled payments with FX converted USD amounts
WITH tx AS (
    SELECT * FROM {{ ref('stg_payments') }}
),
fx AS (
    SELECT * FROM {{ ref('stg_fx_rates') }}
),
merch AS (
    SELECT * FROM {{ ref('stg_merchants') }}
)
SELECT 
    t.transaction_id,
    t.idempotency_key,
    t.transaction_timestamp,
    t.account_id,
    t.merchant_id,
    m.legal_name as merchant_name,
    t.card_brand,
    t.amount as original_amount,
    t.currency,
    coalesce(f.exchange_rate, 1.0) as fx_rate_to_usd,
    round(t.amount / coalesce(f.exchange_rate, 1.0), 2) as amount_usd,
    round((t.amount / coalesce(f.exchange_rate, 1.0)) * m.interchange_rate, 2) as interchange_fee_usd,
    t.status,
    t.country_code,
    t.risk_score,
    t.aml_risk_score,
    t.is_aml_flagged,
    t.aml_reasons
FROM tx t
LEFT JOIN fx f ON t.currency = f.target_currency
LEFT JOIN merch m ON t.merchant_id = m.merchant_id
