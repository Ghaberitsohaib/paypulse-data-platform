-- Fact Table: Daily Merchant Settlement & Net Disbursable Funds
SELECT 
    merchant_id,
    merchant_name,
    count(*) as transaction_count,
    sum(case when status = 'APPROVED' then 1 else 0 end) as approved_count,
    sum(case when status = 'DECLINED' then 1 else 0 end) as declined_count,
    sum(case when is_aml_flagged then 1 else 0 end) as flagged_count,
    round(sum(case when status = 'APPROVED' then amount_usd else 0 end), 2) as gross_volume_usd,
    round(sum(case when status = 'APPROVED' then interchange_fee_usd else 0 end), 2) as processing_fees_usd,
    round(sum(case when status = 'APPROVED' then amount_usd * 0.05 else 0 end), 2) as rolling_reserve_held_usd,
    round(sum(case when status = 'APPROVED' then (amount_usd - interchange_fee_usd - (amount_usd * 0.05)) else 0 end), 2) as net_payout_usd
FROM {{ ref('fct_transactions') }}
GROUP BY merchant_id, merchant_name
ORDER BY gross_volume_usd DESC
