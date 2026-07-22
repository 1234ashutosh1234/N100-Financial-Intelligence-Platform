import sys
import os

sys.path.append(os.path.abspath("."))

from src.analytics.cagr import *


print("Running CAGR Tests...")

# Normal CAGR
assert revenue_cagr(100, 200, 5)[1] == "OK"

# Zero Base
assert revenue_cagr(0, 100, 5)[1] == "ZERO_BASE"

# Turnaround
assert revenue_cagr(-100, 100, 5)[1] == "TURNAROUND"

# Decline to Loss
assert revenue_cagr(100, -100, 5)[1] == "DECLINE_TO_LOSS"

# Both Negative
assert revenue_cagr(-100, -50, 5)[1] == "BOTH_NEGATIVE"

# Missing
assert revenue_cagr(None, 100, 5)[1] == "MISSING"

# PAT
assert pat_cagr(100, 150, 5)[1] == "OK"

# EPS
assert eps_cagr(10, 20, 5)[1] == "OK"

print("All CAGR Tests Passed")