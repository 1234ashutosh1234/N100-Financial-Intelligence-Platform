"""
Sprint 5 QA Validation
"""

from pathlib import Path

files = [
    "output/analysis_parsed.csv",
    "output/parsing_failures.csv",
    "output/pros_cons_generated.csv",
    "output/cashflow_intelligence.xlsx",
    "output/distress_alerts.csv",
    "output/pattern_changes.csv",
    "reports/portfolio/portfolio_summary.pdf",
]

print("=" * 60)
print("Sprint 5 QA")
print("=" * 60)

passed = 0

for file in files:

    if Path(file).exists():
        print(f"✓ {file}")
        passed += 1
    else:
        print(f"✗ {file}")

print()

print(f"Passed : {passed}/{len(files)}")