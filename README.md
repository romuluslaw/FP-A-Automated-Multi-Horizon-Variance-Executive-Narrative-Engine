# 📊 FP&A Automated Multi-Horizon Variance & Executive Narrative Engine

An open-source, zero-cost AI automation solution built for **Financial Planning & Analysis (FP&A)** teams. This engine automates month-end Budget vs. Actuals (BvA) reporting, computes critical working capital drag metrics (DSO, DPO, Turnover ratios), and leverages local, offline LLMs to generate tailored, 3-column stakeholder write-ups (**Leadership, Board of Directors, and Investors**) while enforcing strict **PDPA / PII data anonymization**.

---

## 🎯 Business Case & Executive Summary

### The Problem
During monthly closes and rolling forecast cycles, FP&A teams spend up to **60–70% of their time**:
1. Exporting and normalizing disjointed Excel files across Budget, Forecast, and Actuals.
2. Manually calculating variances across multiple time horizons.
3. Rewriting the exact same financial results into different narrative formats for executives, board members, and external investors.

### The Solution
This showcase project automates the entire ingestion-to-narration pipeline using open-source tools:
* **Zero Software Licensing Cost:** Runs completely on local open-weights LLMs (via Ollama / Llama 3) with an offline fallback mode—eliminating paid API subscriptions (OpenAI, Zapier, etc.).
* **Data Governance & Privacy:** Features an inline PDPA/PII scrubbing engine that redacts vendor names, client identifiers, and bank details prior to external stakeholder exports.
* **Multi-Perspective AI Commentary:** Automatically translates P&L variances and working capital metrics into 3 distinct executive lenses simultaneously.

---

## 🏗 System Architecture & Workflow

```text
+-----------------------------------------------------------------------------------+
|                            1. DATA INGESTION & COA CROSSWALK                      |
|                                                                                   |
|  Source Files: Actuals.xlsx | Budget.xlsx | Forecast.xlsx | coa_mapping.csv       |
|  - Validates period dates & headers to prevent stale file version drift.          |
|  - Maps raw ERP/GL accounts to standard corporate Chart of Accounts (CoA).        |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        2. CALCULATIONS & MATERIALITY ENGINE                       |
|                                                                                   |
|  - Multi-Horizon Variances: MoM, QoQ, vs. Budget ($ & \%), vs. Forecast ($ & %)    |
|  - Working Capital Ratios: DSO, DPO, Debtor Turnover, Payable Turnover            |
|  - Net Cash Drag: Cash Conversion Cycle (DSO - DPO)                               |
|  - Two-Sided Threshold Filter: (|Var $| >= $25k) AND (|Var %| >= 5%)               |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                    3. PDPA SCRUBBING & DUAL-MODE LLM NARRATIVE                    |
|                                                                                   |
|  - PDPA Anonymizer: Scrubs PII, vendor names, and customer details.               |
|  - Local Ollama Driver (Llama 3 / Qwen) + Mock Fallback for CI/CD Testing.        |
|  - Generates 3-Column Stakeholder Perspectives:                                   |
|    • Leadership: Operational levers, cost drivers, and immediate fixes.           |
|    • Board of Directors: High-level strategy, governance, and macro risks.        |
|    • Investors: Capital efficiency, top-line trajectory, anonymized metrics.      |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        4. INTERACTIVE DASHBOARD & EXPORTS                         |
|                                                                                   |
|  - Streamlit Web App (`app.py`) with real-time materiality threshold sliders.     |
|  - Node.js Integration Test Suite (`test.js`) for CI/CD verification.             |
+-----------------------------------------------------------------------------------+




## Repository Directory Structure

fpa-automation-showcase/
├── data/
│   ├── generate_mock_data.py # Script to populate mock multi-tab Excel files
│   ├── actuals.xlsx          # Actuals P&L, Balance Sheet, Cash Flow
│   ├── budget.xlsx           # Annual Master Budget
│   ├── forecast.xlsx         # 12-Month Rolling Forecast
│   └── coa_mapping.csv       # Chart of Accounts Crosswalk
├── engine/
│   ├── ingestion.py          # Data Loader, Period Matcher & CoA Crosswalk
│   ├── variance_ratios.py    # Multi-Horizon Variance, DSO/DPO & Working Capital Drag
│   ├── anonymizer.py         # PDPA / PII Data Redaction Engine
│   └── llm_narrative.py      # Dual-Mode LLM Engine (Live Ollama + Mock Fallback)
├── main.py                   # Pipeline CLI Orchestrator
├── app.py                    # Streamlit Executive Dashboard UI
├── test.js                   # Node.js Integration & Regression Test Suite
├── requirements.txt          # Python Package Dependencies
├── .gitignore                # Git Exclusion Rules
├── LICENSE                   # MIT License
└── README.md                 # Complete System Documentation

## 💡 Key Financial Ratios & Metrics Calculated

| Metric Category | Formula / Logic | CFO Strategic Purpose |
| :--- | :--- | :--- |
| **Gross Margin %** | (Revenue - COGS) / Revenue * 100 | Measures core product pricing power and direct supply cost expansion. |
| **Days Sales Outstanding (DSO)** | (Accounts Receivable / Revenue) * 30 | Tracks collection efficiency and customer payment behavior. |
| **Days Payable Outstanding (DPO)** | (Accounts Payable / COGS) * 30 | Measures supplier credit utilization and cash preservation. |
| **Working Capital Drag** | DSO - DPO | Pinpoints net cash cycle strain before it impacts liquidity. |
| **Debtor Turnover** | Revenue / Accounts Receivable | Evaluates asset utilization speed and receivables velocity. |
| **Payable Turnover** | COGS / Accounts Payable | Monitors vendor credit cycle throughput. |

---

## 🛠️ Step-by-Step Setup Guide (Non-Technical Users)

This guide assumes **zero programming experience**. Follow these steps to get the app running on your computer in under 10 minutes.

### Step 1: Install Required Software (One-time)
1. **Python (Calculation Engine):** Download and install from [python.org](https://www.python.org/downloads/). 
   * ⚠️️ **WINDOWS USERS:** Make sure to check the box **"Add python.exe to PATH"** on the very first screen of the installer.
2. **Node.js (Test Runner):** Download and install the LTS version from [nodejs.org](https://nodejs.org/).

### Step 2: Download & Extract Project
1. Click the green **Code** button at the top of this GitHub repository and select **Download ZIP**.
2. Extract the unzipped folder to your **Desktop**.

### Step 3: Open Terminal / Command Prompt
* **Windows:** Press `Win + R`, type `cmd`, and press **Enter**.
* **Mac:** Press `Cmd + Space`, type `Terminal`, and press **Return**.

Navigate into the project folder by running:
```bash
cd Desktop/fpa-automation-showcase

###Step 4: Install Dependencies & Create Data
1. Copy and paste this command to install all required libraries:
pip install -r requirements.txt

2. Generate the sample 🧪 Integration Testing & Bug Resolution Log
To ensure enterprise-grade stability, all core components are verified using the Node.js Integration Test Suite (test.js). Below are key edge cases identified and resolved during development:

1. Unmapped ERP Account Codes (Silent P&L Drops)
Issue: When raw ERP actuals contained new GL codes absent from coa_mapping.csv, standard inner joins dropped line items silently, underreporting total revenue.

Fix: Implemented a left-join strategy paired with an explicit Audit Warning Logger in engine/ingestion.py that flags unmapped account codes without breaking execution.

2. Zero-Division Handling in Ratio Calculations
Issue: During initial operational months or zero-spend cost centers, zero values in COGS or Accounts Receivable caused ZeroDivisionError crashes when calculating DPO or Turnover ratios.

Fix: Added safety guard clauses (if revenue > 0 else 0.0) across all ratio functions in engine/variance_ratios.py.

3. CI/CD Environment LLM Offline Failures
Issue: Automated testing environments without a running local Ollama instance threw connection errors during AI narrative generation.

Fix: Built a Dual-Mode LLM Module (engine/llm_narrative.py) featuring an offline Mock Fallback Engine triggered via the --mock CLI flag.financial datasets by running:
python data/generate_mock_data.py

### Step 5: Verify via Node.js Test Suite
1. Run the automated integration test suite:
node test.js
When you see ALL INTEGRATION & REGRESSION TESTS PASSED (4/4), your environment is 100% verified!

### Step 6: Launch the Dashboard
Start the interactive Web UI:
streamlit run app.py

Your default browser will automatically open to http://localhost:8501.


##🧪 Integration Testing & Bug Resolution Log
To ensure enterprise-grade stability, all core components are verified using the Node.js Integration Test Suite (test.js). Below are key edge cases identified and resolved during development:

1. Unmapped ERP Account Codes (Silent P&L Drops)
Issue: When raw ERP actuals contained new GL codes absent from coa_mapping.csv, standard inner joins dropped line items silently, underreporting total revenue.

Fix: Implemented a left-join strategy paired with an explicit Audit Warning Logger in engine/ingestion.py that flags unmapped account codes without breaking execution.

2. Zero-Division Handling in Ratio Calculations
Issue: During initial operational months or zero-spend cost centers, zero values in COGS or Accounts Receivable caused ZeroDivisionError crashes when calculating DPO or Turnover ratios.

Fix: Added safety guard clauses (if revenue > 0 else 0.0) across all ratio functions in engine/variance_ratios.py.

3. CI/CD Environment LLM Offline Failures
Issue: Automated testing environments without a running local Ollama instance threw connection errors during AI narrative generation.

Fix: Built a Dual-Mode LLM Module (engine/llm_narrative.py) featuring an offline Mock Fallback Engine triggered via the --mock CLI flag.




