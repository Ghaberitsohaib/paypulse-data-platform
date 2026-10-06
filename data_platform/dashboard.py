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

# Configure page settings
st.set_page_config(
    page_title="PayPulse | Real-Time Payment Lakehouse & AML Platform",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# HIGH-END FINTECH UI DESIGN SYSTEM (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0e1526 0%, #070a12 60%, #05070b 100%);
        color: #f1f5f9;
    }

    /* Top Navigation Banner */
    .top-banner {
        background: linear-gradient(135deg, rgba(20, 29, 49, 0.8) 0%, rgba(13, 19, 33, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
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
        background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .banner-subtitle {
        color: #94a3b8;
        font-size: 0.92rem;
        margin-top: 6px;
        font-weight: 400;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Metric Cards Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }

    .kpi-card {
        background: linear-gradient(145deg, rgba(23, 32, 54, 0.75) 0%, rgba(13, 18, 32, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(12px);
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.15);
    }

    .kpi-card-emerald { border-top: 3px solid #10b981; }
    .kpi-card-indigo  { border-top: 3px solid #6366f1; }
    .kpi-card-cyan    { border-top: 3px solid #06b6d4; }
    .kpi-card-amber   { border-top: 3px solid #f59e0b; }
    .kpi-card-rose    { border-top: 3px solid #f43f5e; }

    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .kpi-icon {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }

    .kpi-icon-emerald { background: rgba(16, 185, 129, 0.15); color: #10b981; }
    .kpi-icon-indigo  { background: rgba(99, 102, 241, 0.15); color: #818cf8; }
    .kpi-icon-cyan    { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }
    .kpi-icon-amber   { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
    .kpi-icon-rose    { background: rgba(244, 63, 94, 0.15); color: #fb7185; }

    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #f8fafc;
        line-height: 1.2;
        font-family: 'JetBrains Mono', 'Plus Jakarta Sans', monospace;
    }

    .kpi-footer {
        margin-top: 10px;
        font-size: 0.78rem;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .kpi-tag-success { color: #10b981; font-weight: 600; }
    .kpi-tag-danger  { color: #f43f5e; font-weight: 600; }

    /* Glass Panels */
    .glass-panel {
        background: linear-gradient(145deg, rgba(20, 28, 48, 0.7) 0%, rgba(11, 16, 28, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }

    /* FinTech Badges */
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-approved { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-declined { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-aml      { background: rgba(244, 63, 94, 0.2); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.4); animation: pulse 1.5s infinite; }

    /* Custom Streamlit adjustments */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 0.88rem;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    div[data-testid="stSidebar"] {
        background-color: #090d16;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATABASE DATA ACCESS LAYER (Zero Concurrency Lock)
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
# SIDEBAR CONTROLS & PIPELINE EXECUTION
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 10px 0 20px 0;">
    <h2 style="font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin: 0; display: flex; align-items: center; gap: 8px;">
        ⚡ Pipeline Control
    </h2>
    <p style="color: #64748b; font-size: 0.8rem; margin: 4px 0 0 0;">Trigger live streaming & distributed batch jobs</p>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("▶ Emit Live Kafka Transactions", use_container_width=True, type="primary"):
    with st.spinner("Emitting 60 sub-second Kafka payment events & updating dbt marts..."):
        from streaming.consumer_to_lakehouse import sink_stream_to_lakehouse
        sink_stream_to_lakehouse(60)
        from analytics_dbt.run_dbt import run_dbt_models
        run_dbt_models()
    st.sidebar.success("✅ 60 transactions streamed and settled!")
    st.rerun()

if st.sidebar.button("🔄 Trigger PySpark Reconciliation", use_container_width=True):
    with st.spinner("Running PySpark batch reconciliation & fee calculation..."):
        from batch.spark_reconciliation_job import run_spark_reconciliation_batch
        run_spark_reconciliation_batch()
    st.sidebar.success("✅ Spark settlement engine finished!")
    st.rerun()

st.sidebar.markdown("---")

# Quick Filters in Sidebar
st.sidebar.markdown("<h3 style='font-size: 0.95rem; font-weight: 700; color: #cbd5e1;'>🔍 Filter Transactions</h3>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOAD & VALIDATION
# -----------------------------------------------------------------------------
if not os.path.exists(DB_PATH):
    st.markdown("""
    <div class="top-banner">
        <div>
            <h1 class="banner-title">💳 PayPulse — Real-Time Payment Lakehouse</h1>
            <p class="banner-subtitle">Warehouse database initializing...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.warning("⚠️ Warehouse database not found yet. Click below to initialize and seed the platform with live mock data.")
    if st.button("🚀 Initialize & Execute End-to-End Pipeline", type="primary"):
        with st.spinner("Bootstrapping complete lakehouse pipeline..."):
            from scripts.run_pipeline import run_entire_pipeline
            run_entire_pipeline()
        st.success("✅ Pipeline successfully initialized!")
        st.rerun()
    st.stop()

tx_df, payout_df, aml_df = load_warehouse_data()

if tx_df is None or len(tx_df) == 0:
    st.info("No transaction data found in warehouse. Please emit transactions from the sidebar.")
    st.stop()

# Interactive filter controls
selected_status = st.sidebar.selectbox("Authorization Status", ["ALL", "APPROVED", "DECLINED"])
selected_currency = st.sidebar.selectbox("Transaction Currency", ["ALL"] + sorted(tx_df['currency'].unique().tolist()))
selected_brand = st.sidebar.selectbox("Card Network", ["ALL"] + sorted(tx_df['card_brand'].unique().tolist()))

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
<div style="background: rgba(15, 23, 42, 0.5); padding: 14px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Infrastructure Status</div>
    <div style="margin-top: 8px; font-size: 0.8rem; display: flex; flex-direction: column; gap: 6px;">
        <div>🟢 <b>Kafka:</b> KRaft Streaming</div>
        <div>🟢 <b>Lakehouse:</b> MinIO Partitioned</div>
        <div>🟢 <b>Batch:</b> PySpark Settlements</div>
        <div>🟢 <b>Marts:</b> dbt Star Schema</div>
        <div>🟢 <b>Engine:</b> DuckDB / BigQuery</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TOP HERO HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="top-banner">
    <div>
        <h1 class="banner-title">
            <span>💳</span> PayPulse Command Center
        </h1>
        <p class="banner-subtitle">
            Enterprise FinTech Lakehouse • Real-Time AML Fraud Radar • Sub-Second Payment Orchestration
        </p>
    </div>
    <div style="display: flex; gap: 12px; align-items: center;">
        <div class="status-pill">
            <span class="pulse-dot"></span>
            LIVE STREAM ACTIVE
        </div>
        <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); color: #818cf8; padding: 6px 14px; border-radius: 9999px; font-size: 0.82rem; font-weight: 600;">
            BASE CURRENCY: USD
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# EXECUTIVE KPI METRICS CARDS
# -----------------------------------------------------------------------------
total_tx = len(tx_df)
approved_tx = len(tx_df[tx_df['status'] == 'APPROVED'])
approval_rate = (approved_tx / total_tx * 100) if total_tx > 0 else 0
gross_volume = tx_df[tx_df['status'] == 'APPROVED']['amount_usd'].sum()
total_fees = tx_df[tx_df['status'] == 'APPROVED']['interchange_fee_usd'].sum()
total_net_payout = payout_df['net_merchant_payout_usd'].sum() if 'net_merchant_payout_usd' in payout_df.columns else (gross_volume - total_fees)
total_aml = len(aml_df)

st.markdown(f"""
<div class="metric-grid">
    <!-- Card 1: Gross Processing Volume -->
    <div class="kpi-card kpi-card-emerald">
        <div class="kpi-header">
            <span class="kpi-title">Gross Volume (GPV)</span>
            <div class="kpi-icon kpi-icon-emerald">💎</div>
        </div>
        <div class="kpi-value">${gross_volume:,.2f}</div>
        <div class="kpi-footer">
            <span class="kpi-tag-success">● Cleared</span>
            <span>All currencies normalized to USD</span>
        </div>
    </div>

    <!-- Card 2: Total Transactions & Approval -->
    <div class="kpi-card kpi-card-indigo">
        <div class="kpi-header">
            <span class="kpi-title">Volume & Auth Rate</span>
            <div class="kpi-icon kpi-icon-indigo">⚡</div>
        </div>
        <div class="kpi-value">{total_tx:,} <span style="font-size: 1rem; color: #94a3b8; font-weight: 500;">txns</span></div>
        <div class="kpi-footer">
            <span class="kpi-tag-success">✓ {approval_rate:.1f}%</span>
            <span>Approval authorization rate</span>
        </div>
    </div>

    <!-- Card 3: Platform Fees Collected -->
    <div class="kpi-card kpi-card-amber">
        <div class="kpi-header">
            <span class="kpi-title">Interchange Revenue</span>
            <div class="kpi-icon kpi-icon-amber">📈</div>
        </div>
        <div class="kpi-value">${total_fees:,.2f}</div>
        <div class="kpi-footer">
            <span style="color: #fbbf24; font-weight: 600;">Avg {(total_fees / gross_volume * 100 if gross_volume > 0 else 0):.2f}%</span>
            <span>Interchange fee take rate</span>
        </div>
    </div>

    <!-- Card 4: Net Merchant Payouts -->
    <div class="kpi-card kpi-card-cyan">
        <div class="kpi-header">
            <span class="kpi-title">Disbursable Payouts</span>
            <div class="kpi-icon kpi-icon-cyan">🏛️</div>
        </div>
        <div class="kpi-value">${total_net_payout:,.2f}</div>
        <div class="kpi-footer">
            <span style="color: #22d3ee; font-weight: 600;">Spark Settled</span>
            <span>Net after 5% rolling reserve</span>
        </div>
    </div>

    <!-- Card 5: AML Threat Radar -->
    <div class="kpi-card kpi-card-rose">
        <div class="kpi-header">
            <span class="kpi-title">AML Threats Flagged</span>
            <div class="kpi-icon kpi-icon-rose">🛡️</div>
        </div>
        <div class="kpi-value" style="color: #fb7185;">{total_aml}</div>
        <div class="kpi-footer">
            <span class="kpi-tag-danger">{(total_aml / total_tx * 100 if total_tx > 0 else 0):.1f}% Risk</span>
            <span>Velocity & micro-testing triggers</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INTERACTIVE ANALYTICS TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Global Payment Flows", 
    "🚨 AML & Fraud Detection Radar", 
    "💰 Merchant Settlement Ledger", 
    "⚡ Atomic Transaction Stream",
    "🏛️ System Architecture"
])

# Plotly theme configuration helper
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
# TAB 1: GLOBAL PAYMENT FLOWS
# -----------------------------------------------------------------------------
with tab1:
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.markdown("""
        <div class="glass-panel">
            <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
                💳 Transaction Volume by Card Brand
            </h3>
            <p style="color: #64748b; font-size: 0.8rem; margin: 0 0 12px 0;">Distribution of Gross Processing Volume across payment networks</p>
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
        fig_brand.update_layout(get_dark_plotly_layout(height=320))
        st.plotly_chart(fig_brand, use_container_width=True)

    with c_right:
        st.markdown("""
        <div class="glass-panel">
            <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
                🌍 Geographic Revenue Distribution
            </h3>
            <p style="color: #64748b; font-size: 0.8rem; margin: 0 0 12px 0;">Processed payment volumes grouped by customer country origin</p>
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
            get_dark_plotly_layout(height=320),
            xaxis=dict(title=None, showgrid=False),
            yaxis=dict(title="Volume (USD)", showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_geo, use_container_width=True)

    # Multi-Currency Distribution & Timeline
    st.markdown("""
    <div class="glass-panel" style="margin-top: 10px;">
        <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
            💱 Multi-Currency Cleared Balances (Base USD Conversion)
        </h3>
        <p style="color: #64748b; font-size: 0.8rem; margin: 0 0 12px 0;">Real-time FX conversion using central bank daily exchange rates</p>
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
            get_dark_plotly_layout(height=240),
            showlegend=False,
            xaxis=dict(title=None, showgrid=False),
            yaxis=dict(title="Total USD", showgrid=True, gridcolor="rgba(255,255,255,0.05)")
        )
        st.plotly_chart(fig_curr, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: AML & FRAUD DETECTION RADAR
# -----------------------------------------------------------------------------
with tab2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(244, 63, 94, 0.1) 0%, rgba(30, 20, 30, 0.3) 100%); border: 1px solid rgba(244, 63, 94, 0.25); border-radius: 14px; padding: 18px 22px; margin-bottom: 20px;">
        <h4 style="color: #fb7185; margin: 0 0 6px 0; font-size: 1.05rem; font-weight: 700; display: flex; align-items: center; gap: 8px;">
            <span>🛡️</span> Real-Time Anti-Money Laundering (AML) Rules Engine
        </h4>
        <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0; line-height: 1.5;">
            PayPulse inspects all incoming Kafka payment streams within <b>sub-50ms sliding windows</b>. Any transaction meeting velocity thresholds (<5s between authorizations), micro card-testing fraud (<$2.00 attempts), or high-risk geographic flags is immediately flagged with immutable reason codes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if len(aml_df) > 0:
        col_aml_top, col_aml_pie = st.columns([2, 1])
        
        with col_aml_top:
            st.markdown("<h4 style='color: #f8fafc; font-size: 0.95rem; font-weight: 700;'>🚨 Flagged Suspicious Activity Stream</h4>", unsafe_allow_html=True)
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
            # Expand multiple reasons
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
                fig_reasons.update_layout(get_dark_plotly_layout(height=290))
                st.plotly_chart(fig_reasons, use_container_width=True)
            else:
                st.success("All flagged events analyzed cleanly.")
    else:
        st.success("✅ Clean health status: No high-risk AML transactions detected in the current stream!")

# -----------------------------------------------------------------------------
# TAB 3: MERCHANT SETTLEMENT & RESERVE LEDGER
# -----------------------------------------------------------------------------
with tab3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(15, 23, 42, 0.4) 100%); border: 1px solid rgba(6, 182, 212, 0.25); border-radius: 14px; padding: 18px 22px; margin-bottom: 20px;">
        <h4 style="color: #22d3ee; margin: 0 0 6px 0; font-size: 1.05rem; font-weight: 700; display: flex; align-items: center; gap: 8px;">
            <span>💰</span> PySpark Settlement Ledger & Merchant Payout Formula
        </h4>
        <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0; line-height: 1.5;">
            <b>Net Merchant Payout</b> = Gross Volume - Interchange Fee (1.5% - 2.9%) - <b>5% Rolling Reserve Holdback</b> (retained for 90 days to shield against fraudulent chargebacks).
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
        
        # Payout Comparison Chart
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
            get_dark_plotly_layout(height=340),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="USD")
        )
        st.plotly_chart(fig_settle, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: ATOMIC TRANSACTION STREAM
# -----------------------------------------------------------------------------
with tab4:
    st.markdown("""
    <div class="glass-panel">
        <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
            🔍 Raw Stream Inspection & Idempotency Audit
        </h3>
        <p style="color: #64748b; font-size: 0.8rem; margin: 0 0 12px 0;">
            Showing individual transaction events landed in Lakehouse (Parquet) and reconciled in dbt marts
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
# TAB 5: SYSTEM ARCHITECTURE
# -----------------------------------------------------------------------------
with tab5:
    st.markdown("""
    <div class="glass-panel">
        <h3 style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin: 0 0 8px 0;">
            🏛️ End-to-End Enterprise FinTech Stack
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
                • <b>dltHub</b>: Automated schema inference & daily central bank FX rate ingestion.<br>
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
