import sys
import os

sys.path.append(os.path.abspath("."))

from src.analytics.cashflow_kpis import *

print("Running Cash Flow KPI Tests...")

# Free Cash Flow
assert free_cash_flow(1000, -200) == 800

# CFO Quality
ratio, label = cfo_quality(150, 100)
assert label == "High Quality"

ratio, label = cfo_quality(70, 100)
assert label == "Moderate"

ratio, label = cfo_quality(20, 100)
assert label == "Accrual Risk"

# CapEx
capex, label = capex_intensity(-10, 1000)
assert label == "Asset Light"

capex, label = capex_intensity(-60, 1000)
assert label == "Moderate"

capex, label = capex_intensity(-150, 1000)
assert label == "Capital Intensive"

# FCF Conversion
assert fcf_conversion(200, 100) == 200

# Capital Allocation
pattern, label = capital_allocation(100, -100, -50)
assert label == "Reinvestor"

pattern, label = capital_allocation(-100, -50, 100)
assert label == "Growth Funded by Debt"

print("All Cash Flow KPI Tests Passed")