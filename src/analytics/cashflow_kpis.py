"""
Cash Flow KPI Library
Sprint 2 - Financial Ratio Engine
"""

import pandas as pd


def safe_divide(a, b):
    if pd.isna(a) or pd.isna(b):
        return None
    if b == 0:
        return None
    return round(a / b, 2)


# ----------------------------------------------------
# FREE CASH FLOW
# ----------------------------------------------------

def free_cash_flow(operating_activity, investing_activity):
    """
    FCF = CFO + CFI
    (Investing Activity is usually negative)
    """
    if pd.isna(operating_activity):
        return None

    if pd.isna(investing_activity):
        investing_activity = 0

    return round(
        operating_activity + investing_activity,
        2
    )


# ----------------------------------------------------
# CFO QUALITY
# ----------------------------------------------------

def cfo_quality(operating_activity, net_profit):

    value = safe_divide(
        operating_activity,
        net_profit
    )

    return value


# ----------------------------------------------------
# CAPEX INTENSITY
# ----------------------------------------------------

def capex_intensity(investing_activity, sales):

    if pd.isna(investing_activity):
        return None

    investing_activity = abs(investing_activity)

    value = safe_divide(
        investing_activity,
        sales
    )

    if value is None:
        return None

    return round(value * 100, 2)


# ----------------------------------------------------
# FCF CONVERSION
# ----------------------------------------------------

def fcf_conversion(fcf, operating_profit):

    value = safe_divide(
        fcf,
        operating_profit
    )

    if value is None:
        return None

    return round(value * 100, 2)


# ----------------------------------------------------
# CAPITAL ALLOCATION
# ----------------------------------------------------

def capital_allocation(
        operating_activity,
        investing_activity,
        financing_activity):

    def sign(v):

        if pd.isna(v):
            return "0"

        if v > 0:
            return "+"

        if v < 0:
            return "-"

        return "0"

    cfo = sign(operating_activity)
    cfi = sign(investing_activity)
    cff = sign(financing_activity)

    if cfo == "+" and cfi == "-" and cff == "-":
        return "Reinvestment"

    if cfo == "+" and cfi == "-" and cff == "+":
        return "Growth Funded by Debt"

    if cfo == "+" and cfi == "+" and cff == "-":
        return "Shareholder Returns"

    if cfo == "+" and cfi == "+" and cff == "+":
        return "Cash Accumulator"

    if cfo == "-" and cfi == "-" and cff == "+":
        return "Distress Signal"

    if cfo == "-" and cfi == "-" and cff == "-":
        return "Pre-Revenue"

    return "Mixed"


# ----------------------------------------------------
# CFO SCORE
# ----------------------------------------------------

def cashflow_score(
        fcf,
        cfo_quality_ratio,
        capex):

    score = 0

    if fcf is not None and fcf > 0:
        score += 40

    if cfo_quality_ratio is not None:

        if cfo_quality_ratio > 1:
            score += 30

        elif cfo_quality_ratio > 0.7:
            score += 20

    if capex is not None:

        if capex < 5:
            score += 30

        elif capex < 10:
            score += 20

    return score


print("Cash Flow KPI Library Loaded Successfully")