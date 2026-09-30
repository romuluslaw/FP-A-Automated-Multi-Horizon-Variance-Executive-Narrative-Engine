import pandas as pd
import numpy as np

def create_mock_excel_files():
    # Chart of Accounts Crosswalk
    coa_map = pd.DataFrame([
        {"ERP_Account_Code": "4000-01", "ERP_Description": "Gross Software Revenue", "Std_Account_Category": "Revenue", "Std_Account_Name": "Product Revenue"},
        {"ERP_Account_Code": "4000-02", "ERP_Description": "Consulting Services Income", "Std_Account_Category": "Revenue", "Std_Account_Name": "Service Revenue"},
        {"ERP_Account_Code": "5000-10", "ERP_Description": "Direct Hosting & Cloud Expense", "Std_Account_Category": "COGS", "Std_Account_Name": "Cost of Goods Sold"},
        {"ERP_Account_Code": "6000-05", "ERP_Description": "Salaries - Engineering & Product", "Std_Account_Category": "OpEx", "Std_Account_Name": "R&D Expense"},
        {"ERP_Account_Code": "6000-20", "ERP_Description": "Digital Marketing & Ad Spend", "Std_Account_Category": "OpEx", "Std_Account_Name": "Sales & Marketing"},
        {"ERP_Account_Code": "6000-90", "ERP_Description": "Executive & Admin Overhead", "Std_Account_Category": "OpEx", "Std_Account_Name": "G&A Expense"},
    ])
    coa_map.to_csv("data/coa_mapping.csv", index=False)

    # 1. P&L Data
    pl_data = {
        "ERP_Account_Code": ["4000-01", "4000-02", "5000-10", "6000-05", "6000-20", "6000-90"],
        "Actuals_Amount": [520000, 110000, 185000, 160000, 145000, 75000],
        "Budget_Amount":  [500000, 150000, 150000, 150000, 110000, 70000],
        "Forecast_Amount": [510000, 120000, 170000, 155000, 130000, 72000]
    }
    df_pl = pd.DataFrame(pl_data)

    # 2. Balance Sheet Metrics (Receivables, Payables)
    bs_data = {
        "Metric": ["Accounts Receivable", "Accounts Payable"],
        "Actuals_Amount": [210000, 125000],
        "Budget_Amount":  [180000, 110000],
        "Forecast_Amount": [195000, 115000]
    }
    df_bs = pd.DataFrame(bs_data)

    # 3. Cash Flow Metrics
    cf_data = {
        "Cash_Flow_Activity": ["Operating Cash Inflow", "Operating Cash Outflow", "Investing Activities", "Financing Activities"],
        "Actuals_Amount": [610000, -480000, -55000, 0],
        "Budget_Amount":  [650000, -430000, -30000, 0],
        "Forecast_Amount": [630000, -450000, -40000, 0]
    }
    df_cf = pd.DataFrame(cf_data)

    # Export Budget, Actuals, Forecast files
    with pd.ExcelWriter("data/actuals.xlsx") as writer:
        df_pl.to_excel(writer, sheet_name="IncomeStatement", index=False)
        df_bs.to_excel(writer, sheet_name="BalanceSheet", index=False)
        df_cf.to_excel(writer, sheet_name="CashFlow", index=False)

    with pd.ExcelWriter("data/budget.xlsx") as writer:
        df_pl.assign(Actuals_Amount=df_pl["Budget_Amount"]).to_excel(writer, sheet_name="IncomeStatement", index=False)
        df_bs.assign(Actuals_Amount=df_bs["Budget_Amount"]).to_excel(writer, sheet_name="BalanceSheet", index=False)
        df_cf.assign(Actuals_Amount=df_cf["Budget_Amount"]).to_excel(writer, sheet_name="CashFlow", index=False)

    with pd.ExcelWriter("data/forecast.xlsx") as writer:
        df_pl.assign(Actuals_Amount=df_pl["Forecast_Amount"]).to_excel(writer, sheet_name="IncomeStatement", index=False)
        df_bs.assign(Actuals_Amount=df_bs["Forecast_Amount"]).to_excel(writer, sheet_name="BalanceSheet", index=False)
        df_cf.assign(Actuals_Amount=df_cf["Forecast_Amount"]).to_excel(writer, sheet_name="CashFlow", index=False)

    print("Mock financial datasets generated successfully in data/")

if __name__ == "__main__":
    create_mock_excel_files()