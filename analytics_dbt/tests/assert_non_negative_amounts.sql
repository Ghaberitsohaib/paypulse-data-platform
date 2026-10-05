-- Singular Test: Ensures all transaction amounts in USD are strictly positive
SELECT 
    transaction_id,
    amount_usd
FROM {{ ref('fct_transactions') }}
WHERE amount_usd <= 0
