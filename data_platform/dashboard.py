import sys, os
from pathlib import Path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import duckdb
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configure page layout
st.set_page_config(
    page_title="PayPulse | Real-Time FinTech & AML Command Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# PROFESSIONAL ENTERPRISE FINTECH DESIGN SYSTEM (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Global Dark Canvas */
.stApp {
    background-color: #070b14 !important;
    background-image: radial-gradient(circle at 10% 10%, #0d1527 0%, #060911 60%, #04060a 100%) !important;
    color: #f8fafc !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #0c1322 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding-top: 1.5rem !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p {
    color: #f1f5f9 !important;
}

section[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #141e33 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #f8fafc !important;
    font-weight: 500 !important;
}

div[data-baseweb="popover"] ul {
    background-color: #141e33 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

div[data-baseweb="popover"] li {
    color: #f8fafc !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: #1e293b !important;
}

/* Action Buttons */
button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 16px !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    transition: all 0.2s ease !important;
}

button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
}

button[kind="secondary"] {
    background: #141e33 !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 16px !important;
    transition: all 0.2s ease !important;
}

button[kind="secondary"]:hover {
    background: #1e293b !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    color: #ffffff !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background-color: #0c1322 !important;
    padding: 6px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 6px !important;
    padding: 8px 16px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: #cbd5e1 !important;
    border: none !important;
    background: transparent !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35) !important;
}

/* Top Banner */
.top-banner {
    background: linear-gradient(135deg, rgba(23, 33, 56, 0.9) 0%, rgba(11, 17, 30, 0.98) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 22px 28px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(16px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.banner-title {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 40%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.banner-subtitle {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-top: 5px;
    font-weight: 400;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Metric Cards */
.kpi-card {
    background: linear-gradient(145deg, rgba(23, 33, 56, 0.85) 0%, rgba(13, 19, 34, 0.98) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, border-color 0.2s ease;
    margin-bottom: 12px;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
}

.kpi-card-emerald { border-top: 3px solid #10b981; }
.kpi-card-indigo  { border-top: 3px solid #6366f1; }
.kpi-card-amber   { border-top: 3px solid #f59e0b; }
.kpi-card-cyan    { border-top: 3px solid #06b6d4; }
.kpi-card-rose    { border-top: 3px solid #f43f5e; }

.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.kpi-title {
    color: #94a3b8;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    white-space: nowrap;
}

.kpi-pill {
    font-size: 0.68rem;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 4px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.kpi-pill-emerald { background: rgba(16, 185, 129, 0.18); color: #34d399; }
.kpi-pill-indigo  { background: rgba(99, 102, 241, 0.18); color: #a5b4fc; }
.kpi-pill-amber   { background: rgba(245, 158, 11, 0.18); color: #fcd34d; }
.kpi-pill-cyan    { background: rgba(6, 182, 212, 0.18); color: #67e8f9; }
.kpi-pill-rose    { background: rgba(244, 63, 94, 0.18); color: #fda4af; }

.kpi-value {
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #f8fafc;
    line-height: 1.2;
    font-family: 'JetBrains Mono', 'Plus Jakarta Sans', monospace;
}

.kpi-value-emerald { color: #34d399; }
.kpi-value-indigo  { color: #a5b4fc; }
.kpi-value-amber   { color: #fcd34d; }
.kpi-value-cyan    { color: #67e8f9; }
.kpi-value-rose    { color: #fda4af; }

.kpi-footer {
    margin-top: 7px;
    font-size: 0.74rem;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 6px;
}

.kpi-tag-success { color: #34d399; font-weight: 600; }
.kpi-tag-danger  { color: #fb7185; font-weight: 600; }

/* Glass Panels & Tables */
.glass-panel {
    background: linear-gradient(145deg, rgba(20, 28, 48, 0.75) 0%, rgba(11, 16, 28, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    margin-bottom: 18px;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATABASE LAYER (Zero Locking)
# -----------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "fintech_warehouse.duckdb")

def load_warehouse_data():
    if not os.path.exists(DB_PATH):
        return None, None, None
    con = duckdb.connect(DB_PATH, read_only=False)
    try:
        tx_df = con.execute("SELECT * FROM fintech_analytics.fct_transactions;").df()
        payout_df = con.execute("SELECT * FROM fintech_analytics.fct_merchant_daily_payouts;").df()
        aml_df = con.execute("SELECT * FROM fintech_analytics.fct_aml_suspicious_activity;").df()
        return tx_df, payout_df, aml_df
    finally:
        con.close()

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 6px 0 16px 0;">
    <h2 style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin: 0; letter-spacing: -0.01em;">
        Pipeline Console
    </h2>
    <p style="color: #94a3b8; font-size: 0.78rem; margin: 4px 0 0 0;">Streaming ingestion & batch settlement</p>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Emit Kafka Stream (60 Events)", use_container_width=True, type="primary"):
    with st.spinner("Emitting Kafka payment events and syncing dbt marts..."):
        from streaming.consumer_to_lakehouse import sink_stream_to_lakehouse
        sink_stream_to_lakehouse(60)
        from analytics_dbt.run_dbt import run_dbt_models
        run_dbt_models()
    st.sidebar.success("60 transactions streamed and reconciled.")
    st.rerun()

if st.sidebar.button("Run PySpark Reconciliation", use_container_width=True):
    with st.spinner("Executing PySpark batch settlement and reserve calculation..."):
        from batch.spark_reconciliation_job import run_spark_reconciliation_batch
        run_spark_reconciliation_batch()
    st.sidebar.success("PySpark settlement completed.")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='font-size: 0.85rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;'>Transaction Filters</h3>", unsafe_allow_html=True)

# Validate DB exists
if not os.path.exists(DB_PATH):
    st.warning("Warehouse database not initialized.")
    if st.button("Initialize Lakehouse Pipeline", type="primary"):
        with st.spinner("Executing end-to-end pipeline initialization..."):
            from scripts.run_pipeline import run_entire_pipeline
            run_entire_pipeline()
        st.rerun()
    st.stop()

tx_df, payout_df, aml_df = load_warehouse_data()
if tx_df is None or len(tx_df) == 0:
    st.info("No transaction data found in warehouse.")
    st.stop()

# Interactive filter controls
selected_status = st.sidebar.selectbox("Authorization Status", ["ALL", "APPROVED", "DECLINED"])
selected_currency = st.sidebar.selectbox("Currency", ["ALL"] + sorted(tx_df['currency'].unique().tolist()))
selected_brand = st.sidebar.selectbox("Card Brand", ["ALL"] + sorted(tx_df['card_brand'].unique().tolist()))

# Apply filters
filtered_tx = tx_df.copy()
if selected_status != "ALL":
    filtered_tx = filtered_tx[filtered_tx['status'] == selected_status]
if selected_currency != "ALL":
    filtered_tx = filtered_tx[filtered_tx['currency'] == selected_currency]
if selected_brand != "ALL":
    filtered_tx = filtered_tx[filtered_tx['card_brand'] == selected_brand]

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: rgba(20, 30, 50, 0.7); padding: 12px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08);">
    <div style="color: #94a3b8; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Infrastructure Status</div>
    <div style="margin-top: 8px; font-size: 0.8rem; display: flex; flex-direction: column; gap: 6px;">
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Kafka:</b> <span style="color:#94a3b8;">KRaft Streaming</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Lakehouse:</b> <span style="color:#94a3b8;">MinIO Parquet</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Batch:</b> <span style="color:#94a3b8;">PySpark Settlements</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Marts:</b> <span style="color:#94a3b8;">dbt Star Schema</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Engine:</b> <span style="color:#94a3b8;">DuckDB / BigQuery</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HERO HEADER BANNER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="top-banner">
    <div>
        <h1 class="banner-title">PayPulse Command Center</h1>
        <p class="banner-subtitle">
            Enterprise FinTech Lakehouse • Real-Time AML Fraud Detection • Payment Stream Orchestration
        </p>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <div class="status-pill">
            <span class="pulse-dot"></span>
            LIVE STREAM ACTIVE
        </div>
        <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.35); color: #a5b4fc; padding: 5px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.03em;">
            BASE CURRENCY: USD
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# EXECUTIVE KPI METRICS
# -----------------------------------------------------------------------------
total_tx = len(tx_df)
approved_tx = len(tx_df[tx_df['status'] == 'APPROVED'])
approval_rate = (approved_tx / total_tx * 100) if total_tx > 0 else 0
gross_volume = tx_df[tx_df['status'] == 'APPROVED']['amount_usd'].sum()
total_fees = tx_df[tx_df['status'] == 'APPROVED']['interchange_fee_usd'].sum()
total_net_payout = payout_df['net_merchant_payout_usd'].sum() if 'net_merchant_payout_usd' in payout_df.columns else (gross_volume - total_fees)
total_aml = len(aml_df)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
<div class="kpi-card kpi-card-emerald">
    <div class="kpi-header">
        <span class="kpi-title">Gross Volume (GPV)</span>
        <span class="kpi-pill kpi-pill-emerald">USD</span>
    </div>
    <div class="kpi-value kpi-value-emerald">${gross_volume:,.2f}</div>
    <div class="kpi-footer">
        <span class="kpi-tag-success">Cleared</span>
        <span>Normalized to Base USD</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
<div class="kpi-card kpi-card-indigo">
    <div class="kpi-header">
        <span class="kpi-title">Volume & Auth Rate</span>
        <span class="kpi-pill kpi-pill-indigo">AUTH</span>
    </div>
    <div class="kpi-value kpi-value-indigo">{total_tx:,} <span style="font-size: 0.95rem; color: #94a3b8;">txns</span></div>
    <div class="kpi-footer">
        <span class="kpi-tag-success">{approval_rate:.1f}%</span>
        <span>Authorization rate</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
<div class="kpi-card kpi-card-amber">
    <div class="kpi-header">
        <span class="kpi-title">Interchange Revenue</span>
        <span class="kpi-pill kpi-pill-amber">FEES</span>
    </div>
    <div class="kpi-value kpi-value-amber">${total_fees:,.2f}</div>
    <div class="kpi-footer">
        <span style="color: #fbbf24; font-weight: 600;">{(total_fees / gross_volume * 100 if gross_volume > 0 else 0):.2f}%</span>
        <span>Platform take rate</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
<div class="kpi-card kpi-card-cyan">
    <div class="kpi-header">
        <span class="kpi-title">Disbursable Payouts</span>
        <span class="kpi-pill kpi-pill-cyan">NET</span>
    </div>
    <div class="kpi-value kpi-value-cyan">${total_net_payout:,.2f}</div>
    <div class="kpi-footer">
        <span style="color: #22d3ee; font-weight: 600;">Spark Settled</span>
        <span>Net after 5% reserve</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c5:
    st.markdown(f"""
<div class="kpi-card kpi-card-rose">
    <div class="kpi-header">
        <span class="kpi-title">AML Threats Flagged</span>
        <span class="kpi-pill kpi-pill-rose">RISK</span>
    </div>
    <div class="kpi-value kpi-value-rose">{total_aml}</div>
    <div class="kpi-footer">
        <span class="kpi-tag-danger">{(total_aml / total_tx * 100 if total_tx > 0 else 0):.1f}% Risk</span>
        <span>Velocity & micro tests</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PLOTLY THEME CONFIG
# -----------------------------------------------------------------------------
def get_dark_plotly_layout(height=340):
    return dict(
        height=height,
        margin=dict(l=15, r=15, t=35, b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="#94a3b8", size=12),
        hoverlabel=dict(bgcolor="#1e293b", font_color="#f8fafc", font_size=12)
    )

# -----------------------------------------------------------------------------
# TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Global Payment Flows", 
    "AML Fraud Radar", 
    "Merchant Settlement Ledger", 
    "Transaction Stream Audit",
    "System Architecture"
])

# -----------------------------------------------------------------------------
# TAB 1: FLOWS
# -----------------------------------------------------------------------------
with tab1:
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Transaction Volume by Card Brand
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Distribution of Gross Processing Volume across payment networks</p>
</div>
""", unsafe_allow_html=True)
        brand_df = filtered_tx.groupby("card_brand")['amount_usd'].sum().reset_index()
        fig_brand = px.pie(
            brand_df, 
            names="card_brand", 
            values="amount_usd", 
            hole=0.55,
            color="card_brand",
            color_discrete_map={
                "VISA": "#3b82f6", 
                "MASTERCARD": "#f97316", 
                "AMEX": "#10b981", 
                "DISCOVER": "#8b5cf6"
            }
        )
        fig_brand.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='#0b0f19', width=2))
        )
        fig_brand.update_layout(**get_dark_plotly_layout(height=310))
        st.plotly_chart(fig_brand, use_container_width=True)

    with c_right:
        st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Geographic Volume Distribution
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Processed payment volumes grouped by customer country origin</p>
</div>
""", unsafe_allow_html=True)
        geo_df = filtered_tx.groupby("country_code")['amount_usd'].sum().reset_index().sort_values(by="amount_usd", ascending=False)
        fig_geo = px.bar(
            geo_df,
            x="country_code",
            y="amount_usd",
            text_auto='.2s',
            color="amount_usd",
            color_continuous_scale=["#312e81", "#6366f1", "#06b6d4", "#10b981"]
        )
        fig_geo.update_layout(
            xaxis=dict(title=None, showgrid=False),
            yaxis=dict(title="Volume (USD)", showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            coloraxis_showscale=False,
            **get_dark_plotly_layout(height=310)
        )
        st.plotly_chart(fig_geo, use_container_width=True)

    # Multi-Currency Distribution
    st.markdown("""
<div class="glass-panel" style="margin-top: 14px;">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Multi-Currency Cleared Balances (Base USD)
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Real-time FX conversion using central bank daily exchange rates</p>
</div>
""", unsafe_allow_html=True)
    
    curr_summary = filtered_tx.groupby("currency").agg(
        tx_count=('transaction_id', 'count'),
        original_sum=('original_amount', 'sum'),
        usd_sum=('amount_usd', 'sum')
    ).reset_index()
    curr_summary['avg_ticket_usd'] = (curr_summary['usd_sum'] / curr_summary['tx_count']).round(2)
    
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        st.dataframe(
            curr_summary.style.format({
                'original_sum': '{:,.2f}',
                'usd_sum': '${:,.2f}',
                'avg_ticket_usd': '${:,.2f}'
            }),
            use_container_width=True
        )
    with col_c2:
        fig_curr = px.bar(
            curr_summary,
            x="currency",
            y="usd_sum",
            color="currency",
            color_discrete_sequence=["#10b981", "#6366f1", "#f59e0b", "#ec4899"]
        )
        fig_curr.update_layout(
            showlegend=False,
            xaxis=dict(title=None, showgrid=False),
            yaxis=dict(title="Total USD", showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            **get_dark_plotly_layout(height=240)
        )
        st.plotly_chart(fig_curr, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: AML RADAR
# -----------------------------------------------------------------------------
with tab2:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(244, 63, 94, 0.12) 0%, rgba(30, 20, 30, 0.4) 100%); border: 1px solid rgba(244, 63, 94, 0.3); border-radius: 12px; padding: 18px 22px; margin-bottom: 20px;">
    <h4 style="color: #fb7185; margin: 0 0 6px 0; font-size: 1.05rem; font-weight: 700;">
        Real-Time Anti-Money Laundering (AML) Rules Engine
    </h4>
    <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0; line-height: 1.5;">
        PayPulse inspects all incoming Kafka payment streams within <b>sub-50ms sliding windows</b>. Any transaction meeting velocity thresholds (<5s between authorizations), micro card-testing fraud (<$2.00 attempts), or high-risk geographic flags is flagged with immutable reason codes.
    </p>
</div>
""", unsafe_allow_html=True)

    if len(aml_df) > 0:
        col_aml_top, col_aml_pie = st.columns([2, 1])
        
        with col_aml_top:
            st.markdown("<h4 style='color: #f8fafc; font-size: 0.95rem; font-weight: 700;'>Flagged Suspicious Activity Stream</h4>", unsafe_allow_html=True)
            display_aml = aml_df[[
                'transaction_id', 'transaction_timestamp', 'merchant_name', 'card_brand', 
                'amount_usd', 'country_code', 'aml_risk_score', 'aml_reasons'
            ]].copy()
            st.dataframe(
                display_aml.style.format({'amount_usd': '${:,.2f}'}),
                use_container_width=True
            )

        with col_aml_pie:
            st.markdown("<h4 style='color: #f8fafc; font-size: 0.95rem; font-weight: 700;'>Threat Breakdown by Trigger</h4>", unsafe_allow_html=True)
            all_reasons = []
            for r in aml_df['aml_reasons']:
                for sub in str(r).split(';'):
                    cleaned = sub.strip()
                    if cleaned and cleaned != 'NORMAL_TRANSACTION':
                        all_reasons.append(cleaned)
            if all_reasons:
                reason_df = pd.Series(all_reasons).value_counts().reset_index()
                reason_df.columns = ['Trigger Reason', 'Occurrences']
                fig_reasons = px.pie(
                    reason_df,
                    names="Trigger Reason",
                    values="Occurrences",
                    hole=0.45,
                    color_discrete_sequence=["#f43f5e", "#fb923c", "#facc15"]
                )
                fig_reasons.update_layout(**get_dark_plotly_layout(height=290))
                st.plotly_chart(fig_reasons, use_container_width=True)
    else:
        st.success("Status normal: No high-risk AML transactions detected in the active stream.")

# -----------------------------------------------------------------------------
# TAB 3: SETTLEMENT LEDGER
# -----------------------------------------------------------------------------
with tab3:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(15, 23, 42, 0.4) 100%); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 12px; padding: 18px 22px; margin-bottom: 20px;">
    <h4 style="color: #22d3ee; margin: 0 0 6px 0; font-size: 1.05rem; font-weight: 700;">
        PySpark Settlement Ledger & Merchant Payout Formula
    </h4>
    <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0; line-height: 1.5;">
        <b>Net Merchant Payout</b> = Gross Volume - Interchange Fee (1.5% - 2.9%) - <b>5% Rolling Reserve Holdback</b> (retained for 90 days to shield against chargebacks).
    </p>
</div>
""", unsafe_allow_html=True)

    if len(payout_df) > 0:
        st.dataframe(
            payout_df.style.format({
                'gross_volume_usd': '${:,.2f}',
                'processing_fees_usd': '${:,.2f}',
                'rolling_reserve_held_usd': '${:,.2f}',
                'net_payout_usd': '${:,.2f}'
            }),
            use_container_width=True
        )
        
        st.markdown("<h4 style='color: #f8fafc; font-size: 0.95rem; font-weight: 700; margin-top: 15px;'>Gross Volume vs. Net Disbursable Payout by Merchant</h4>", unsafe_allow_html=True)
        fig_settle = go.Figure()
        fig_settle.add_trace(go.Bar(
            name='Gross Volume',
            x=payout_df['merchant_name'],
            y=payout_df['gross_volume_usd'],
            marker_color='#6366f1'
        ))
        fig_settle.add_trace(go.Bar(
            name='Net Payout',
            x=payout_df['merchant_name'],
            y=payout_df['net_payout_usd'],
            marker_color='#10b981'
        ))
        fig_settle.add_trace(go.Bar(
            name='5% Reserve Held',
            x=payout_df['merchant_name'],
            y=payout_df['rolling_reserve_held_usd'],
            marker_color='#f59e0b'
        ))
        fig_settle.update_layout(
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="USD"),
            **get_dark_plotly_layout(height=340)
        )
        st.plotly_chart(fig_settle, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: ATOMIC TRANSACTION STREAM
# -----------------------------------------------------------------------------
with tab4:
    st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Raw Stream Inspection & Idempotency Audit
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">
        Individual transaction events landed in Lakehouse (Parquet) and reconciled in dbt marts
    </p>
</div>
""", unsafe_allow_html=True)

    stream_view = filtered_tx.sort_values(by="transaction_timestamp", ascending=False).head(100)
    st.dataframe(
        stream_view[[
            'transaction_id', 'idempotency_key', 'transaction_timestamp', 'merchant_name', 
            'card_brand', 'original_amount', 'currency', 'fx_rate_to_usd', 'amount_usd', 
            'interchange_fee_usd', 'status', 'country_code', 'risk_score', 'is_aml_flagged'
        ]].style.format({
            'original_amount': '{:,.2f}',
            'amount_usd': '${:,.2f}',
            'interchange_fee_usd': '${:,.2f}',
            'fx_rate_to_usd': '{:.4f}'
        }),
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# TAB 5: ARCHITECTURE
# -----------------------------------------------------------------------------
with tab5:
    st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin: 0 0 8px 0;">
        End-to-End Enterprise FinTech Stack
    </h3>
    <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.6;">
        PayPulse was engineered according to modern lakehouse architectural patterns, delivering resilient sub-second processing and full ACID auditability for high-volume payment rails.
    </p>
</div>
""", unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; height: 100%;">
    <div style="color: #6366f1; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">1. Ingestion & Streaming</div>
    <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.5;">
        • <b>Apache Kafka (KRaft)</b>: High-throughput payment authorizations & terminal events.<br>
        • <b>dltHub</b>: Automated schema inference & daily FX rate ingestion.<br>
        • <b>Real-Time AML</b>: Sliding-window threat detector before persistence.
    </p>
</div>
""", unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; height: 100%;">
    <div style="color: #06b6d4; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">2. Multi-Tier Lakehouse</div>
    <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.5;">
        • <b>Bronze Layer</b>: Raw partitioned Parquet files sinked into MinIO.<br>
        • <b>PySpark Distributed Engine</b>: Aggregates daily payouts & calculates interchange fee holdbacks.<br>
        • <b>Gold Ledger</b>: Cleared settlement ledgers ready for banking dispatch.
    </p>
</div>
""", unsafe_allow_html=True)
    with col_m3:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; height: 100%;">
    <div style="color: #10b981; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">3. Analytics & Orchestration</div>
    <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.5;">
        • <b>dbt (Data Build Tool)</b>: Modular dimensional star schema (staging, dimensions, facts).<br>
        • <b>Data Quality Tests</b>: Automated assertions on transaction amounts & keys.<br>
        • <b>Kestra DAGs</b>: Declarative orchestrator for end-to-end lakehouse schedules.
    </p>
</div>
""", unsafe_allow_html=True)
