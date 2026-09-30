"""
Dual-Mode LLM Narrative Generation Engine.
Supports Live Ollama SDK Execution with an Offline Mock Engine for CI/CD Testing.
"""
import os
from engine.anonymizer import scrub_sensitive_financial_data

def generate_stakeholder_narratives(analysis_result: dict, use_mock: bool = False) -> dict:
    """
    Generates tailored 3-column executive narratives for:
    1. Leadership Team (CFO/CEO/Ops)
    2. Board of Directors (Governance & Risk)
    3. Investors (Growth, Capital Efficiency & PDPA Anonymized)
    """
    material_items = analysis_result["material_variances"]
    ratios = analysis_result["financial_ratios"]

    if use_mock:
        return {
            "Leadership": f"[MOCK AI] Operational Action Required: Cost of Goods Sold expanded vs budget. DSO stands at {ratios['DSO_Days']} days. Recommend tightening client credit terms.",
            "Board": f"[MOCK AI] Governance Summary: Gross Margin achieved {ratios['Gross_Margin_%']}%. Working capital drag is {ratios['Working_Capital_Drag_Days']} days. Overall budget execution remains within regulatory boundaries.",
            "Investors": scrub_sensitive_financial_data(f"[MOCK AI] Performance Update: Revenue growth driven by software expansion. Capital conversion cycle monitored with DSO at {ratios['DSO_Days']} days.")
        }

    # Live Ollama Production Driver
    try:
        import ollama
        prompt_context = f"Material Variances: {material_items}. Key Ratios: {ratios}."
        
        leadership_res = ollama.generate(model="llama3.2", prompt=f"Act as CFO. Write an operational directive for executive leadership based on: {prompt_context}")
        board_res = ollama.generate(model="llama3.2", prompt=f"Act as CFO. Write a strategic risk report for the Board of Directors based on: {prompt_context}")
        investor_raw = ollama.generate(model="llama3.2", prompt=f"Act as CFO. Write an investor update on growth and capital efficiency based on: {prompt_context}")
        
        return {
            "Leadership": leadership_res["response"],
            "Board": board_res["response"],
            "Investors": scrub_sensitive_financial_data(investor_raw["response"])
        }
    except Exception as e:
        print(f"[Ollama Driver Warning]: Fallback to Mock Engine due to error: {e}")
        return generate_stakeholder_narratives(analysis_result, use_mock=True)