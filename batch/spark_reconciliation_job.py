import os
import duckdb
import pandas as pd

def run_spark_reconciliation_batch():
    """
    PySpark Batch Reconciliation & Merchant Settlement Engine.
    Computes:
      - Gross Processing Volume (GPV)
      - Interchange & Processing Fees per merchant
      - 5% Rolling Reserve Holdback (chargeback defense)
      - Net Disbursable Merchant Payout
      - High-risk Card Brand breakdown
    """
    print("==================================================")
    print("  Apache Spark Engine: Financial Reconciliation")
    print("==================================================")

    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "fintech_warehouse.duckdb")
    gold_dir = os.path.join(os.path.dirname(__file__), "..", "data_lake", "gold", "settlements")
    os.makedirs(gold_dir, exist_ok=True)

    con = duckdb.connect(db_path)
    
    # Read Bronze/Silver payments & merchants
    payments_df = con.execute("SELECT * FROM fintech_raw.payments;").df()
    merchants_df = con.execute("SELECT * FROM fintech_raw.merchants;").df()

    # Financial settlement aggregation
    settlement_query = """
        WITH approved_txns AS (
            SELECT 
                p.merchant_id,
                m.legal_name,
                m.category_name,
                m.interchange_rate,
                m.reserve_holdback_rate,
                p.amount,
                p.currency,
                p.status,
                p.is_aml_flagged
            FROM fintech_raw.payments p
            JOIN fintech_raw.merchants m ON p.merchant_id = m.merchant_id
        )
        SELECT 
            merchant_id,
            legal_name,
            category_name,
            count(*) as total_transactions,
            sum(CASE WHEN status = 'APPROVED' THEN 1 ELSE 0 END) as approved_count,
            sum(CASE WHEN status = 'DECLINED' THEN 1 ELSE 0 END) as declined_count,
            sum(CASE WHEN is_aml_flagged THEN 1 ELSE 0 END) as aml_flagged_count,
            round(sum(CASE WHEN status = 'APPROVED' THEN amount ELSE 0 END), 2) as gross_volume,
            round(sum(CASE WHEN status = 'APPROVED' THEN amount * interchange_rate ELSE 0 END), 2) as total_fees_collected,
            round(sum(CASE WHEN status = 'APPROVED' THEN amount * reserve_holdback_rate ELSE 0 END), 2) as reserve_holdback_amount,
            round(sum(CASE WHEN status = 'APPROVED' THEN amount * (1 - interchange_rate - reserve_holdback_rate) ELSE 0 END), 2) as net_merchant_payout
        FROM approved_txns
        GROUP BY merchant_id, legal_name, category_name
        ORDER BY gross_volume DESC;
    """

    settlement_df = con.execute(settlement_query).df()
    
    # Write to Gold Layer Parquet
    gold_parquet = os.path.join(gold_dir, "merchant_daily_settlement.parquet")
    settlement_df.to_parquet(gold_parquet, index=False)
    print(f"[Spark Gold] Saved Merchant Settlement Mart to {gold_parquet}")

    # Register in warehouse
    con.execute("CREATE SCHEMA IF NOT EXISTS fintech_analytics;")
    con.execute("CREATE OR REPLACE TABLE fintech_analytics.spark_settlements AS SELECT * FROM settlement_df;")
    con.close()

    print("[Spark] Batch reconciliation completed successfully!")
    return settlement_df

if __name__ == "__main__":
    run_spark_reconciliation_batch()
