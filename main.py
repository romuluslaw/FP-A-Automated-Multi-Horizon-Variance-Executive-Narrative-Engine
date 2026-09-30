"""
Main FP&A Pipeline Orchestrator CLI.
Accepts optional --mock flag for CI/CD testing environments.
"""
import sys
import json
from engine.ingestion import load_and_map_financial_data
from engine.variance_ratios import compute_variances_and_ratios
from engine.llm_narrative import generate_stakeholder_narratives

def run_fpa_pipeline(use_mock: bool = False):
    # 1. Ingest Data
    raw_data = load_and_map_financial_data(
        "data/actuals.xlsx", "data/budget.xlsx", "data/forecast.xlsx", "data/coa_mapping.csv"
    )
    # 2. Compute Variances & Ratios
    analysis = compute_variances_and_ratios(raw_data, abs_threshold=25000.0, rel_threshold=0.05)
    
    # 3. Generate Narratives
    narratives = generate_stakeholder_narratives(analysis, use_mock=use_mock)

    output = {
        "status": "SUCCESS",
        "ratios": analysis["financial_ratios"],
        "material_variances_count": len(analysis["material_variances"]),
        "narratives": narratives
    }

    print(json.dumps(output, indent=2))
    return output

if __name__ == "__main__":
    use_mock_flag = "--mock" in sys.argv
    run_fpa_pipeline(use_mock=use_mock_flag)