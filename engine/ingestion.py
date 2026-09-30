"""
Ingestion & Chart of Accounts (CoA) Crosswalk Engine.
Auditable Data Loading & Period Validation.
"""
import pandas as pd
import os

def load_and_map_financial_data(actuals_path: str, budget_path: str, forecast_path: str, coa_map_path: str) -> dict:
    """
    Loads raw ERP/Excel data files, applies Chart of Accounts (CoA) reclassification mapping,
    and returns standardized financial DataFrames for Income Statement, Balance Sheet, and Cash Flow.
    
    Audit Trail: Logs unmapped ERP account codes to prevent silent reconciliation drops.
    """
    if not all([os.path.exists(p) for p in [actuals_path, budget_path, forecast_path, coa_map_path]]):
        raise FileNotFoundError("One or more required Excel/CSV input files are missing.")

    # Load CoA Crosswalk
    coa_df = pd.read_csv(coa_map_path)
    
    # Load Actuals, Budget, Forecast
    act_pl = pd.read_excel(actuals_path, sheet_name="IncomeStatement")
    bud_pl = pd.read_excel(budget_path, sheet_name="IncomeStatement")
    fct_pl = pd.read_excel(forecast_path, sheet_name="IncomeStatement")

    # Merge P&L Actuals, Budget, Forecast
    merged_pl = act_pl.merge(bud_pl[['ERP_Account_Code', 'Actuals_Amount']], on='ERP_Account_Code', suffixes=('', '_Bud'))
    merged_pl = merged_pl.merge(fct_pl[['ERP_Account_Code', 'Actuals_Amount']], on='ERP_Account_Code', suffixes=('_Act', '_Fct'))
    merged_pl.rename(columns={'Actuals_Amount_Act': 'Actuals', 'Actuals_Amount_Bud': 'Budget', 'Actuals_Amount_Fct': 'Forecast'}, inplace=True)

    # Apply CoA Mapping
    mapped_pl = merged_pl.merge(coa_df, on='ERP_Account_Code', how='left')
    
    # Check for Unmapped Accounts (Audit Guard)
    unmapped = mapped_pl[mapped_pl['Std_Account_Name'].isna()]
    if not unmapped.empty:
        print(f"[AUDIT WARNING]: {len(unmapped)} account codes missing from CoA Crosswalk!")

    # Rollup to Standard Accounts
    summary_pl = mapped_pl.groupby(['Std_Account_Category', 'Std_Account_Name'])[['Actuals', 'Budget', 'Forecast']].sum().reset_index()

    # Load Balance Sheet & Cash Flow
    act_bs = pd.read_excel(actuals_path, sheet_name="BalanceSheet").rename(columns={'Actuals_Amount': 'Actuals'})
    act_cf = pd.read_excel(actuals_path, sheet_name="CashFlow").rename(columns={'Actuals_Amount': 'Actuals'})

    return {
        "pl_summary": summary_pl,
        "balance_sheet": act_bs,
        "cash_flow": act_cf
    }