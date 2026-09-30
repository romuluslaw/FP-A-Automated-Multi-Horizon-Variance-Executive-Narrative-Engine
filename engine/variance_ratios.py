"""
Multi-Horizon Variance & Working Capital Ratio Engine.
Computes absolute/relative variance, DSO, DPO, Turnover Ratios, and Working Capital Drag.
"""
import pandas as pd

def compute_variances_and_ratios(data_dict: dict, abs_threshold: float = 25000.0, rel_threshold: float = 0.05) -> dict:
    """
    Computes:
    1. Multi-horizon variances (vs Budget & vs Forecast) for $, %
    2. Two-sided materiality filtering (|Var $| >= Threshold AND |Var %| >= Threshold)
    3. Working capital metrics: DSO, DPO, Debtor Turnover, Payable Turnover, Cash Drag.
    """
    df_pl = data_dict["pl_summary"].copy()

    # Variance Calculations
    df_pl["Var_Bud_$"] = df_pl["Actuals"] - df_pl["Budget"]
    df_pl["Var_Bud_%"] = (df_pl["Var_Bud_$"] / df_pl["Budget"].replace(0, 1)).round(4)
    
    df_pl["Var_Fct_$"] = df_pl["Actuals"] - df_pl["Forecast"]
    df_pl["Var_Fct_%"] = (df_pl["Var_Fct_$"] / df_pl["Forecast"].replace(0, 1)).round(4)

    # Materiality Filter Check (Two-Sided)
    df_pl["Material_Flag"] = (df_pl["Var_Bud_$"].abs() >= abs_threshold) & (df_pl["Var_Bud_%"].abs() >= rel_threshold)
    material_variances = df_pl[df_pl["Material_Flag"] == True].to_dict(orient="records")

    # Working Capital & Ratios Computation
    df_bs = data_dict["balance_sheet"].set_index("Metric")["Actuals"].to_dict()
    
    revenue = df_pl[df_pl["Std_Account_Category"] == "Revenue"]["Actuals"].sum()
    cogs = df_pl[df_pl["Std_Account_Category"] == "COGS"]["Actuals"].sum()
    ar = df_bs.get("Accounts Receivable", 0)
    ap = df_bs.get("Accounts Payable", 0)

    # 30-Day Monthly Standard Horizon
    dso = round((ar / revenue * 30), 2) if revenue > 0 else 0.0
    dpo = round((ap / cogs * 30), 2) if cogs > 0 else 0.0
    debtor_turnover = round((revenue / ar), 2) if ar > 0 else 0.0
    payable_turnover = round((cogs / ap), 2) if ap > 0 else 0.0
    working_capital_drag = round(dso - dpo, 2)

    ratios = {
        "Gross_Margin_%": round(((revenue - cogs) / revenue * 100), 2) if revenue > 0 else 0.0,
        "DSO_Days": dso,
        "DPO_Days": dpo,
        "Debtor_Turnover_x": debtor_turnover,
        "Payable_Turnover_x": payable_turnover,
        "Working_Capital_Drag_Days": working_capital_drag
    }

    return {
        "pl_analysis": df_pl,
        "material_variances": material_variances,
        "financial_ratios": ratios
    }