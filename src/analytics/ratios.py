import pandas as pd
import numpy as np


# -------------------------------
# Net Profit Margin
# -------------------------------
def net_profit_margin(net_profit, sales):
    if pd.isna(net_profit) or pd.isna(sales):
        return None

    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


# -------------------------------
# Operating Profit Margin
# -------------------------------
def operating_profit_margin(op_profit, sales):
    if pd.isna(op_profit) or pd.isna(sales):
        return None

    if sales == 0:
        return None

    return round((op_profit / sales) * 100, 2)


# -------------------------------
# Return on Equity
# -------------------------------
def roe(net_profit, equity):
    if pd.isna(net_profit) or pd.isna(equity):
        return None

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


# -------------------------------
# Return on Capital Employed
# -------------------------------
def roce(ebit, equity, borrowings):
    if pd.isna(ebit):
        return None

    capital = equity + borrowings

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


# -------------------------------
# Return on Assets
# -------------------------------
def roa(net_profit, total_assets):
    if pd.isna(net_profit) or pd.isna(total_assets):
        return None

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)

# ---------------------------------
# Debt to Equity Ratio
# ---------------------------------
def debt_to_equity(borrowings, equity):
    if pd.isna(borrowings) or pd.isna(equity):
        return None

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)


# ---------------------------------
# Interest Coverage Ratio
# ---------------------------------
def interest_coverage(operating_profit, interest):
    if pd.isna(operating_profit) or pd.isna(interest):
        return None

    if interest == 0:
        return None

    return round(operating_profit / interest, 2)


# ---------------------------------
# Net Debt
# ---------------------------------
def net_debt(borrowings, investments):
    if pd.isna(borrowings):
        return None

    if pd.isna(investments):
        investments = 0

    return round(borrowings - investments, 2)


# ---------------------------------
# Asset Turnover
# ---------------------------------
def asset_turnover(sales, total_assets):
    if pd.isna(sales) or pd.isna(total_assets):
        return None

    if total_assets == 0:
        return None

    return round(sales / total_assets, 2)


# ---------------------------------
# High Leverage Flag
# ---------------------------------
def high_leverage_flag(de_ratio):
    if de_ratio is None:
        return False

    return de_ratio > 5


# ---------------------------------
# ICR Warning Flag
# ---------------------------------
def icr_warning(icr):
    if icr is None:
        return False

    return icr < 1.5