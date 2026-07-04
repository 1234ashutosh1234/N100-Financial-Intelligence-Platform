"""
Financial Ratio Functions
Sprint 2 - Financial Ratio Engine
"""

import pandas as pd


def safe_divide(a, b):
    """Safely divide two numbers."""
    if pd.isna(a) or pd.isna(b):
        return None
    if b == 0:
        return None
    return round(a / b, 2)


# ----------------------------
# PROFITABILITY RATIOS
# ----------------------------

def net_profit_margin(net_profit, sales):
    value = safe_divide(net_profit, sales)
    return None if value is None else round(value * 100, 2)


def operating_profit_margin(operating_profit, sales):
    value = safe_divide(operating_profit, sales)
    return None if value is None else round(value * 100, 2)


def roe(net_profit, equity):
    value = safe_divide(net_profit, equity)
    return None if value is None else round(value * 100, 2)


def roce(ebit, capital_employed):
    value = safe_divide(ebit, capital_employed)
    return None if value is None else round(value * 100, 2)


def roa(net_profit, total_assets):
    value = safe_divide(net_profit, total_assets)
    return None if value is None else round(value * 100, 2)


# ----------------------------
# LEVERAGE RATIOS
# ----------------------------

def debt_to_equity(total_debt, equity):
    return safe_divide(total_debt, equity)


def interest_coverage(ebit, interest):
    return safe_divide(ebit, interest)


def debt_ratio(total_liabilities, total_assets):
    return safe_divide(total_liabilities, total_assets)


def equity_ratio(equity, total_assets):
    return safe_divide(equity, total_assets)


def net_debt(total_debt, investments):
    if pd.isna(total_debt):
        return None
    if pd.isna(investments):
        investments = 0
    return round(total_debt - investments, 2)


# ----------------------------
# EFFICIENCY RATIOS
# ----------------------------

def asset_turnover(sales, total_assets):
    return safe_divide(sales, total_assets)


def capital_turnover(sales, capital_employed):
    return safe_divide(sales, capital_employed)


def fixed_asset_turnover(sales, fixed_assets):
    return safe_divide(sales, fixed_assets)


# ----------------------------
# SHAREHOLDER RATIOS
# ----------------------------

def book_value_per_share(networth, equity_capital):
    return safe_divide(networth, equity_capital)


def earnings_per_share(net_profit, equity_capital):
    return safe_divide(net_profit, equity_capital)


def dividend_payout(dividend, net_profit):
    value = safe_divide(dividend, net_profit)
    return None if value is None else round(value * 100, 2)


# ----------------------------
# GROWTH RATIOS
# ----------------------------

def revenue_growth(current_sales, previous_sales):
    if previous_sales == 0 or pd.isna(previous_sales):
        return None
    return round(((current_sales - previous_sales) / previous_sales) * 100, 2)


def profit_growth(current_profit, previous_profit):
    if previous_profit == 0 or pd.isna(previous_profit):
        return None
    return round(((current_profit - previous_profit) / previous_profit) * 100, 2)


# ----------------------------
# HEALTH SCORE
# ----------------------------

def health_score(roe_pct, debt_equity, npm):
    score = 0

    if roe_pct is not None:
        if roe_pct > 20:
            score += 40
        elif roe_pct > 15:
            score += 30
        elif roe_pct > 10:
            score += 20

    if debt_equity is not None:
        if debt_equity < 0.5:
            score += 30
        elif debt_equity < 1:
            score += 20

    if npm is not None:
        if npm > 20:
            score += 30
        elif npm > 10:
            score += 20

    return score


# ----------------------------
# QUALITY SCORE
# ----------------------------

def quality_score(roe_pct, debt_equity, interest_cov):

    score = 0

    if roe_pct and roe_pct > 15:
        score += 40

    if debt_equity is not None and debt_equity < 1:
        score += 30

    if interest_cov and interest_cov > 5:
        score += 30

    return score


print("Financial Ratio Library Loaded Successfully")