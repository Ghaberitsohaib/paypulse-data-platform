import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from batch.spark_reconciliation_job import run_spark_reconciliation_batch

if __name__ == "__main__":
    run_spark_reconciliation_batch()
