import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from ingestion.dlt_fx_rates_pipeline import run_dlt_ingestion
from streaming.consumer_to_lakehouse import sink_stream_to_lakehouse

def seed():
    print("Seeding initial FinTech master and transaction data...")
    run_dlt_ingestion()
    sink_stream_to_lakehouse(80)

if __name__ == "__main__":
    seed()
