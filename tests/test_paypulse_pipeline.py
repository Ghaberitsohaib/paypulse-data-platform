import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
import os
import duckdb
import pytest
from scripts.run_pipeline import run_entire_pipeline

@pytest.fixture(scope="module")
def execute_pipeline():
    run_entire_pipeline()
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "fintech_warehouse.duckdb")
    return duckdb.connect(db_path, read_only=True)

def test_merchants_ingested(execute_pipeline):
    con = execute_pipeline
    count = con.execute("SELECT count(*) FROM fintech_raw.merchants;").fetchone()[0]
    assert count >= 10, "Expected at least 10 merchants"

def test_fx_rates_available(execute_pipeline):
    con = execute_pipeline
    count = con.execute("SELECT count(*) FROM fintech_raw.fx_rates;").fetchone()[0]
    assert count >= 4, "Expected at least 4 FX rates"

def test_transactions_normalized(execute_pipeline):
    con = execute_pipeline
    res = con.execute("SELECT count(*), min(amount_usd) FROM fintech_analytics.fct_transactions;").fetchone()
    total, min_amt = res
    assert total > 0, "Transactions should exist"
    assert min_amt > 0, "No negative transactions allowed"

def test_merchant_settlement_ledger(execute_pipeline):
    con = execute_pipeline
    count = con.execute("SELECT count(*) FROM fintech_analytics.fct_merchant_daily_payouts;").fetchone()[0]
    assert count > 0, "Merchant settlements must be computed"
