import os
import duckdb
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="PayPulse — FinTech & AML Intelligence",
    page_icon="[FINTECH]",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Neon FinTech Aesthetic)
st.markdown("""
<style>
    .main { background-color: #0b0f19; color: #f3f4f6; }
    .stMetric {
        background-color: #131b2e;
        border: 1px solid #1f293d;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .badge-approved { background-color: #10b981; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
    .badge-flagged { background-color: #ef4444; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Database Connection
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "fintech_warehouse.duckdb")

def get_connection():
    if not os.path.exists(DB_PATH):
        return None
    return duckdb.connect(DB_PATH, read_only=True)

st.title("[FINTECH] PayPulse — Real-Time Payment Lakehouse & AML Command Center")
st.caption("Enterprise FinTech Intelligence • Apache Kafka • MinIO Lakehouse • PySpark • dbt • DuckDB")

con = get_connection()

if con is None:
    st.warning("⚠️ Warehouse database not found yet. Run the end-to-end pipeline from the sidebar to initialize data!")
    if st.button("[START] Initialize & Run Pipeline Now"):
        from scripts.run_pipeline import run_entire_pipeline
        run_entire_pipeline()
        st.rerun()
    st.stop()

# Sidebar Controls
st.sidebar.header("[RUN] Pipeline Execution Controls")
if st.sidebar.button("▶ Emit Live Kafka Transactions"):
    from streaming.consumer_to_lakehouse import sink_stream_to_lakehouse
    sink_stream_to_lakehouse(60)
    from analytics_dbt.run_dbt import run_dbt_models
    run_dbt_models()
    st.sidebar.success("Emitted 60 live transactions and synced dbt marts!")
    st.rerun()

if st.sidebar.button("🔄 Trigger Spark Reconciliation"):
    from batch.spark_reconciliation_job import run_spark_reconciliation_batch
    run_spark_reconciliation_batch()
    st.sidebar.success("Spark batch reconciliation completed!")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("""
**Architecture Breakdown**:
- **Streaming**: Kafka + Real-Time AML
- **Lakehouse**: MinIO Bronze/Silver/Gold
- **Batch**: PySpark Distributed Settlement
- **Modeling**: dbt Star Schema
- **Warehouse**: DuckDB / GCP BigQuery
""")

# Key Financial Metrics
try:
    tx_df = con.execute("SELECT * FROM fintech_analytics.fct_transactions;").df()
    payout_df = con.execute("SELECT * FROM fintech_analytics.fct_merchant_daily_payouts;").df()
    aml_df = con.execute("SELECT * FROM fintech_analytics.fct_aml_suspicious_activity;").df()
except Exception as e:
    st.error(f"Error loading marts: {e}")
    st.stop()

total_tx = len(tx_df)
approved_tx = len(tx_df[tx_df['status'] == 'APPROVED'])
approval_rate = (approved_tx / total_tx * 100) if total_tx > 0 else 0
gross_volume = tx_df[tx_df['status'] == 'APPROVED']['amount_usd'].sum()
total_fees = tx_df[tx_df['status'] == 'APPROVED']['interchange_fee_usd'].sum()
total_aml = len(aml_df)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Transactions", f"{total_tx:,}")
c2.metric("Approval Rate", f"{approval_rate:.1f}%")
c3.metric("Gross Volume (USD)", f"${gross_volume:,.2f}")
c4.metric("Fees Collected", f"${total_fees:,.2f}")
c5.metric("AML Fraud Alerts", f"{total_aml}", delta=f"{total_aml} flagged", delta_color="inverse")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Analytics", "[ALERT] Real-Time AML Fraud Monitor", "[MONEY] Merchant Settlement Ledger", "[SEARCH] Live Stream Inspector"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Transaction Volume by Card Brand")
        card_fig = px.pie(tx_df, names="card_brand", values="amount_usd", hole=0.45,
                          color_discrete_sequence=["#3b82f6", "#10b981", "#f59e0b"])
        card_fig.update_layout(paper_bgcolor="#131b2e", plot_bgcolor="#131b2e", font_color="#ffffff")
        st.plotly_chart(card_fig, use_container_width=True)

    with col_b:
        st.subheader("Transaction Distribution by Country")
        geo_fig = px.bar(tx_df.groupby("country_code")['amount_usd'].sum().reset_index(),
                         x="country_code", y="amount_usd", color="amount_usd",
                         color_continuous_scale="Purples")
        geo_fig.update_layout(paper_bgcolor="#131b2e", plot_bgcolor="#131b2e", font_color="#ffffff")
        st.plotly_chart(geo_fig, use_container_width=True)

with tab2:
    st.subheader("[ALERT] Anti-Money Laundering (AML) & Fraud Radar")
    st.write("Real-time detections of rapid card velocity, micro-testing, and high-risk geographical sanctions.")
    if len(aml_df) > 0:
        st.dataframe(
            aml_df[['transaction_id', 'transaction_timestamp', 'merchant_name', 'card_brand', 'amount_usd', 'country_code', 'aml_risk_score', 'aml_reasons']],
            use_container_width=True
        )
    else:
        st.success("No active AML suspicious activities detected.")

with tab3:
    st.subheader("[MONEY] Merchant Daily Settlement Ledger (Spark Gold Model)")
    st.dataframe(payout_df, use_container_width=True)

with tab4:
    st.subheader("[SEARCH] Atomic Streamed Transactions Feed")
    st.dataframe(tx_df.sort_values(by="transaction_timestamp", ascending=False).head(50), use_container_width=True)
