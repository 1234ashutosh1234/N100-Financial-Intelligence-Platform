import sys
import os

sys.path.append(os.path.abspath("."))

from src.analytics.ratios import *


def run_tests():

    print("Running Profitability Ratio Tests...")

    assert net_profit_margin(50, 100) == 50.0
    assert net_profit_margin(10, 0) is None

    assert operating_profit_margin(20, 100) == 20.0
    assert operating_profit_margin(20, 0) is None

    assert roe(50, 200) == 25.0
    assert roe(50, -100) is None

    assert roce(40, 100, 100) == 20.0
    assert roce(40, 0, 0) is None

    assert roa(20, 100) == 20.0
    assert roa(20, 0) is None

    print("All Profitability Tests Passed")


if __name__ == "__main__":
    run_tests()