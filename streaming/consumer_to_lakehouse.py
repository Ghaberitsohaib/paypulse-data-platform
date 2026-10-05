import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
import os
from datetime import datetime, timezone
import pandas as pd
import duckdb
from streaming.payment_producer import run_producer
from streaming.aml_fraud_detector import AMLFraudDetector

def sink_stream_to_lakehouse(num_records: int = 100):
    """
    Consumes Kafka stream transactions, runs real-time AML scoring,
    and writes partitioned Parquet to Bronze Data Lakehouse.
    """
    lake_dir = os.path.join(os.path.dirname(__file__), "..", "data_lake", "bronze", "payments")
    os.makedirs(lake_dir, exist_ok=True)
    
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "fintech_warehouse.duckdb")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print("==================================================")
    print("  Streaming Sink: Kafka -> MinIO Lakehouse (Bronze)")
    print("==================================================")

    # 1. Produce streaming events
    raw_events = run_producer(num_records, delay_sec=0.001)

    # 2. Real-time AML scoring
    detector = AMLFraudDetector(high_risk_threshold=70)
    scored_events = []
    aml_alerts = []

    for tx in raw_events:
        aml_eval = detector.inspect_transaction(tx)
        tx["aml_risk_score"] = aml_eval["final_risk_score"]
        tx["is_aml_flagged"] = aml_eval["is_flagged_aml"]
        tx["aml_reasons"] = aml_eval["reasons"]
        scored_events.append(tx)
        
        if aml_eval["is_flagged_aml"]:
            aml_alerts.append(aml_eval)

    df_payments = pd.DataFrame(scored_events)
    df_aml = pd.DataFrame(aml_alerts) if aml_alerts else pd.DataFrame(columns=[
        "transaction_id", "account_id", "merchant_id", "amount", "currency", 
        "final_risk_score", "is_flagged_aml", "reasons", "evaluated_at"
    ])

    # 3. Partitioned Lakehouse sink (Parquet)
    now = datetime.now(timezone.utc)
    part_dir = os.path.join(lake_dir, f"year={now.year}", f"month={now.month:02d}", f"day={now.day:02d}")
    os.makedirs(part_dir, exist_ok=True)
    parquet_path = os.path.join(part_dir, f"payments_{int(now.timestamp())}.parquet")
    df_payments.to_parquet(parquet_path, index=False, engine="pyarrow")
    print(f"[Lakehouse] Saved {len(df_payments)} records to {parquet_path}")

    # 4. Sync to DuckDB Raw Landing
    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS fintech_raw;")
    con.execute("CREATE OR REPLACE TABLE fintech_raw.payments AS SELECT * FROM df_payments;")
    con.execute("CREATE OR REPLACE TABLE fintech_raw.aml_alerts AS SELECT * FROM df_aml;")
    con.close()

    print(f"[Sink] Stream landed: {len(df_payments)} payments, {len(aml_alerts)} AML fraud alerts.")

if __name__ == "__main__":
    sink_stream_to_lakehouse(50)
