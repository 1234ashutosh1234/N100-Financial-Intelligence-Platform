import pandas as pd
import numpy as np


def calculate_cagr(start_value, end_value, years):
    """
    Returns:
        (cagr_value, flag)
    """

    if years <= 0:
        return None, "INVALID"

    if pd.isna(start_value) or pd.isna(end_value):
        return None, "MISSING"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return round(cagr, 2), "OK"


def revenue_cagr(start_revenue, end_revenue, years):
    return calculate_cagr(start_revenue, end_revenue, years)


def pat_cagr(start_pat, end_pat, years):
    return calculate_cagr(start_pat, end_pat, years)


def eps_cagr(start_eps, end_eps, years):
    return calculate_cagr(start_eps, end_eps, years)