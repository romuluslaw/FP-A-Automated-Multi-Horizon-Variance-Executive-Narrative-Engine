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

