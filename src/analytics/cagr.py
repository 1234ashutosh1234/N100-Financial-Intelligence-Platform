"""
CAGR Engine
Sprint 2
"""

import pandas as pd


def calculate_cagr(start_value, end_value, years):
    """
    CAGR Formula:
    ((End / Start) ** (1 / Years) - 1) * 100
    """

    if pd.isna(start_value) or pd.isna(end_value):
        return None

    if start_value <= 0:
        return None

    if years <= 0:
        return None

    try:
        cagr = ((end_value / start_value) ** (1 / years) - 1) * 100
        return round(cagr, 2)
    except:
        return None


def revenue_cagr(start_sales, end_sales, years):
    return calculate_cagr(start_sales, end_sales, years)


def pat_cagr(start_profit, end_profit, years):
    return calculate_cagr(start_profit, end_profit, years)


def eps_cagr(start_eps, end_eps, years):
    return calculate_cagr(start_eps, end_eps, years)


def growth_flag(value):
    if value is None:
        return "INSUFFICIENT"

    if value > 15:
        return "HIGH"

    if value > 8:
        return "MEDIUM"

    if value > 0:
        return "LOW"

    return "NEGATIVE"


def turnaround(start_profit, end_profit):

    if start_profit < 0 and end_profit > 0:
        return "TURNAROUND"

    if start_profit > 0 and end_profit < 0:
        return "DECLINE"

    if start_profit < 0 and end_profit < 0:
        return "LOSS"

    return "NORMAL"


print("CAGR Engine Loaded Successfully")