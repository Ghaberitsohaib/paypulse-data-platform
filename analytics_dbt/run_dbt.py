import os
import duckdb

def run_dbt_models():
    """
    Python dbt compilation & transformation runner targeting DuckDB warehouse.
    """
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "fintech_warehouse.duckdb")
    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS fintech_analytics;")

    print("==================================================")
    print("  dbt Engine: Running Staging & Mart Transformations")
    print("==================================================")

    # 1. Staging
    con.execute("""
        CREATE OR REPLACE VIEW fintech_analytics.stg_payments AS
        SELECT 
            transaction_id, idempotency_key, cast(timestamp as TIMESTAMP) as transaction_timestamp,
            account_id, merchant_id, card_brand, card_bin, card_last4,
            cast(amount as DECIMAL(12,2)) as amount, upper(currency) as currency,
            upper(status) as status, country_code, risk_score,
            cast(aml_risk_score as INTEGER) as aml_risk_score, is_aml_flagged, aml_reasons, ip_address
        FROM fintech_raw.payments;
    """)

    con.execute("""
        CREATE OR REPLACE VIEW fintech_analytics.stg_merchants AS
        SELECT 
            merchant_id, legal_name, mcc_code, category_name, country_code,
            cast(interchange_rate as DECIMAL(6,4)) as interchange_rate,
            cast(reserve_holdback_rate as DECIMAL(6,4)) as reserve_holdback_rate,
            payout_schedule, kyc_verified, cast(registered_at as TIMESTAMP) as registered_at
        FROM fintech_raw.merchants;
    """)

    con.execute("""
        CREATE OR REPLACE VIEW fintech_analytics.stg_fx_rates AS
        SELECT 
            base_currency, target_currency, cast(exchange_rate as DECIMAL(10,4)) as exchange_rate,
            cast(rate_date as DATE) as rate_date
        FROM fintech_raw.fx_rates;
    """)

    # 2. Marts
    con.execute("""
        CREATE OR REPLACE TABLE fintech_analytics.fct_transactions AS
        SELECT 
            t.transaction_id, t.idempotency_key, t.transaction_timestamp, t.account_id, t.merchant_id,
            m.legal_name as merchant_name, t.card_brand, t.amount as original_amount, t.currency,
            coalesce(f.exchange_rate, 1.0) as fx_rate_to_usd,
            round(t.amount / coalesce(f.exchange_rate, 1.0), 2) as amount_usd,
            round((t.amount / coalesce(f.exchange_rate, 1.0)) * m.interchange_rate, 2) as interchange_fee_usd,
            t.status, t.country_code, t.risk_score, t.aml_risk_score, t.is_aml_flagged, t.aml_reasons
        FROM fintech_analytics.stg_payments t
        LEFT JOIN fintech_analytics.stg_fx_rates f ON t.currency = f.target_currency
        LEFT JOIN fintech_analytics.stg_merchants m ON t.merchant_id = m.merchant_id;
    """)

    con.execute("""
        CREATE OR REPLACE TABLE fintech_analytics.fct_merchant_daily_payouts AS
        SELECT 
            merchant_id, merchant_name, count(*) as transaction_count,
            sum(case when status = 'APPROVED' then 1 else 0 end) as approved_count,
            sum(case when status = 'DECLINED' then 1 else 0 end) as declined_count,
            sum(case when is_aml_flagged then 1 else 0 end) as flagged_count,
            round(sum(case when status = 'APPROVED' then amount_usd else 0 end), 2) as gross_volume_usd,
            round(sum(case when status = 'APPROVED' then interchange_fee_usd else 0 end), 2) as processing_fees_usd,
            round(sum(case when status = 'APPROVED' then amount_usd * 0.05 else 0 end), 2) as rolling_reserve_held_usd,
            round(sum(case when status = 'APPROVED' then (amount_usd - interchange_fee_usd - (amount_usd * 0.05)) else 0 end), 2) as net_payout_usd
        FROM fintech_analytics.fct_transactions
        GROUP BY merchant_id, merchant_name
        ORDER BY gross_volume_usd DESC;
    """)

    con.execute("""
        CREATE OR REPLACE TABLE fintech_analytics.fct_aml_suspicious_activity AS
        SELECT 
            transaction_id, transaction_timestamp, account_id, merchant_id, merchant_name,
            card_brand, original_amount, currency, amount_usd, country_code,
            aml_risk_score, aml_reasons
        FROM fintech_analytics.fct_transactions
        WHERE is_aml_flagged = true OR aml_risk_score >= 70
        ORDER BY aml_risk_score DESC;
    """)

    # Tests
    failed_tests = con.execute("""
        SELECT count(*) FROM fintech_analytics.fct_transactions WHERE amount_usd <= 0;
    """).fetchone()[0]

    if failed_tests > 0:
        raise ValueError(f"dbt test assertion failed: {failed_tests} non-positive transactions found!")

    payouts_count = con.execute("SELECT count(*) FROM fintech_analytics.fct_merchant_daily_payouts;").fetchone()[0]
    tx_count = con.execute("SELECT count(*) FROM fintech_analytics.fct_transactions;").fetchone()[0]
    con.close()

    print(f"[dbt] Built fct_transactions ({tx_count} rows)")
    print(f"[dbt] Built fct_merchant_daily_payouts ({payouts_count} merchants)")
    print("[dbt] All data quality test assertions passed (0 errors)!")

if __name__ == "__main__":
    run_dbt_models()
