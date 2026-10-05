-- Dimension Table: Card intelligence and fraud indices
SELECT 
    concat(card_bin, '-', card_last4) as card_fingerprint,
    card_brand,
    card_bin,
    card_last4,
    count(*) as total_attempts,
    sum(case when status = 'APPROVED' then 1 else 0 end) as approved_tx_count,
    sum(case when status = 'DECLINED' then 1 else 0 end) as declined_tx_count,
    avg(risk_score) as avg_risk_score,
    max(is_aml_flagged) as has_aml_incident
FROM {{ ref('stg_payments') }}
GROUP BY card_bin, card_last4, card_brand
