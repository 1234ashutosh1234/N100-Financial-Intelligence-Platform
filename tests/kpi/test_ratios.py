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

        # -----------------------------
    # Day 9 Tests
    # -----------------------------

    assert debt_to_equity(100, 50) == 2.0
    assert debt_to_equity(100, 0) is None

    assert interest_coverage(100, 20) == 5.0
    assert interest_coverage(100, 0) is None

    assert net_debt(500, 100) == 400
    assert net_debt(500, None) == 500

    assert asset_turnover(1000, 200) == 5.0
    assert asset_turnover(1000, 0) is None

    assert high_leverage_flag(6) is True
    assert high_leverage_flag(3) is False

    assert icr_warning(1.2) is True
    assert icr_warning(2.5) is False