"""
FP&A Automated Planning & Executive Narrative Dashboard
Interactive Streamlit Showcase UI
"""

import streamlit as st
import pandas as pd
import json
import os

# Import core engine modules
from engine.ingestion import load_and_map_financial_data
from engine.variance_ratios import compute_variances_and_ratios
from engine.llm_narrative import generate_stakeholder_narratives

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FP&A Executive Narrative & Variance Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .narrative-box {
        background-color: #ffffff;
        border-left: 4px solid #0d6efd;
        padding: 16px;
        border-radius: 4px;
        font-size: 0.95rem;
        line-height: 1.5;
        min-height: 200px;
    }
    .stTable {
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("📊 Automated FP&A Executive Engine")
st.caption("Multi-Horizon Variance Analysis, Working Capital Ratios & 3-Column Stakeholder Narratives")
st.divider()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ Control Panel")

# Dynamic Materiality Thresholds
st.sidebar.subheader("Materiality Filters")
abs_thresh = st.sidebar.slider(
    "Absolute Variance Threshold ($)",
    min_value=5000,
    max_value=100000,
    value=25000,
    step=5000,
    help="Flags line items where absolute dollar variance exceeds this amount."
)

rel_thresh = st.sidebar.slider(
    "Relative Variance Threshold (%)",
    min_value=1.0,
    max_value=20.0,
    value=5.0,
    step=0.5,
    help="Flags line items where percentage variance exceeds this threshold."
) / 100.0

# Execution Mode
st.sidebar.divider()
st.sidebar.subheader("LLM Engine Mode")
use_mock = st.sidebar.toggle(
    "Mock AI Fallback Mode",
    value=True,
    help="Enable for fast offline demo/testing without requiring a running local Ollama instance."
)

# --- DATA PROCESSING PIPELINE ---
@st.cache_data(ttl=300)
def process_financials(abs_val, rel_val):
    actuals_p = "data/actuals.xlsx"
    budget_p = "data/budget.xlsx"
    forecast_p = "data/forecast.xlsx"
    coa_p = "data/coa_mapping.csv"

    if not all([os.path.exists(p) for p in [actuals_p, budget_p, forecast_p, coa_p]]):
        return None, "Missing input files in `data/`. Please run data generator first."

    try:
        raw_data = load_and_map_financial_data(actuals_p, budget_p, forecast_p, coa_p)
        analysis = compute_variances_and_ratios(raw_data, abs_threshold=abs_val, rel_threshold=rel_val)
        return analysis, None
    except Exception as e:
        return None, str(e)

# Run Pipeline
analysis_results, error_msg = process_financials(abs_thresh, rel_thresh)

if error_msg:
    st.error(f"❌ Pipeline Execution Error: {error_msg}")
    st.info("💡 Run `python data/generate_mock_data.py` to create sample datasets.")
    st.stop()

ratios = analysis_results["financial_ratios"]
df_pl = analysis_results["pl_analysis"]
material_items = analysis_results["material_variances"]

# --- SECTION 1: EXECUTIVE RATIOS & WORKING CAPITAL KPI DASHBOARD ---
st.subheader("💡 Key Financial & Working Capital Ratios")

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.metric(
        label="Gross Margin %",
        value=f"{ratios['Gross_Margin_%']}%",
        delta="Target > 60%"
    )

with kpi_col2:
    st.metric(
        label="DSO (Days)",
        value=f"{ratios['DSO_Days']} Days",
        delta="Receivables",
        delta_color="off"
    )

with kpi_col3:
    st.metric(
        label="DPO (Days)",
        value=f"{ratios['DPO_Days']} Days",
        delta="Payables",
        delta_color="off"
    )

with kpi_col4:
    st.metric(
        label="Working Capital Drag",
        value=f"{ratios['Working_Capital_Drag_Days']} Days",
        delta=f"DSO - DPO",
        delta_color="inverse"
    )

with kpi_col5:
    st.metric(
        label="Debtor Turnover",
        value=f"{ratios['Debtor_Turnover_x']}x",
        delta=f"Payable: {ratios['Payable_Turnover_x']}x",
        delta_color="off"
    )

st.divider()

# --- SECTION 2: 3-COLUMN STAKEHOLDER NARRATIVE ENGINE ---
st.subheader("📝 Tailored Executive Narratives")
st.caption("AI-generated commentary customized for specific stakeholder lenses")

with st.spinner("Generating tailored narratives..."):
    narratives = generate_stakeholder_narratives(analysis_results, use_mock=use_mock)

col_lead, col_board, col_inv = st.columns(3)

with col_lead:
    st.markdown("### 👔 Leadership Team")
    st.caption("**Focus:** Operational Levers, Cost Drivers & Execution")
    st.info(narratives["Leadership"])

with col_board:
    st.markdown("### 🏛️ Board of Directors")
    st.caption("**Focus:** Strategic Governance, Macro Trends & Risk")
    st.warning(narratives["Board"])

with col_inv:
    st.markdown("### 📈 Investors (PDPA Scrubbed)")
    st.caption("**Focus:** Capital Efficiency, Revenue & Privacy Compliance")
    st.success(narratives["Investors"])

st.divider()

# --- SECTION 3: MULTI-HORIZON VARIANCE ANALYSIS TABLE ---
st.subheader("🔍 P&L Line-Item Variance Analysis")
st.caption(f"Highlighting items exceeding **${abs_thresh:,}** AND **{rel_thresh*100:.1f}%** threshold")

# Format DataFrame for Display
display_df = df_pl.copy()
display_df["Actuals"] = display_df["Actuals"].map("${:,.2f}".format)
display_df["Budget"] = display_df["Budget"].map("${:,.2f}".format)
display_df["Forecast"] = display_df["Forecast"].map("${:,.2f}".format)
display_df["Var_Bud_$"] = display_df["Var_Bud_$"].map("${:,.2f}".format)
display_df["Var_Bud_%"] = (display_df["Var_Bud_%"] * 100).map("{:.2f}%".format)

# Highlight Material Rows
def highlight_material(row):
    if row["Material_Flag"]:
        return ['background-color: #fff3cd'] * len(row)
    return [''] * len(row)

styled_table = display_df.style.apply(highlight_material, axis=1)

st.dataframe(
    styled_table,
    column_config={
        "Std_Account_Category": "Category",
        "Std_Account_Name": "Account Name",
        "Var_Bud_$": "Var vs Bud ($)",
        "Var_Bud_%": "Var vs Bud (%)",
        "Material_Flag": "Material Alert"
    },
    use_container_width=True,
    hide_index=True
)

st.caption(f"📌 Found **{len(material_items)}** material line items requiring operational review.")