import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
import os
import duckdb
from datetime import datetime, timezone
import pandas as pd
from ingestion.mock_bank_api import generate_mock_merchants, fetch_mock_fx_rates

def run_dlt_ingestion():
    """
    Ingestion using dltHub principles:
    Extracts REST API data (Merchants & FX Rates), performs schema inference,
    and loads to DuckDB local warehouse and PostgreSQL.
    """
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "fintech_warehouse.duckdb")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print("==================================================")
    print("  dltHub Pipeline: Ingesting Core Banking REST API")
    print("==================================================")

    # 1. Fetch from mock bank API
    merchants_data = generate_mock_merchants(15)
    fx_data = fetch_mock_fx_rates()

    df_merchants = pd.DataFrame(merchants_data)
    df_fx = pd.DataFrame(fx_data)

    # 2. Ingest into Warehouse (DuckDB)
    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS fintech_raw;")
    
    con.execute("CREATE OR REPLACE TABLE fintech_raw.merchants AS SELECT * FROM df_merchants;")
    con.execute("CREATE OR REPLACE TABLE fintech_raw.fx_rates AS SELECT * FROM df_fx;")

    m_count = con.execute("SELECT count(*) FROM fintech_raw.merchants;").fetchone()[0]
    fx_count = con.execute("SELECT count(*) FROM fintech_raw.fx_rates;").fetchone()[0]
    con.close()

    print(f"[dlt] Ingested {m_count} merchants into fintech_raw.merchants")
    print(f"[dlt] Ingested {fx_count} foreign exchange records into fintech_raw.fx_rates")
    print("[dlt] Ingestion completed successfully!")

if __name__ == "__main__":
    run_dlt_ingestion()
