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