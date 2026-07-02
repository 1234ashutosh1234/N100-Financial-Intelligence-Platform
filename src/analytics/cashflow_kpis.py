import pandas as pd


# ---------------------------------
# Free Cash Flow
# ---------------------------------
def free_cash_flow(cfo, investing_activity):
    """
    FCF = CFO + Investing Activity
    (Investing Activity is normally negative)
    """
    if pd.isna(cfo) or pd.isna(investing_activity):
        return None

    return round(cfo + investing_activity, 2)


# ---------------------------------
# CFO Quality Score
# ---------------------------------
def cfo_quality(cfo, pat):
    """
    CFO/PAT Ratio

    >1.0 = High Quality
    0.5-1.0 = Moderate
    <0.5 = Accrual Risk
    """

    if pd.isna(cfo) or pd.isna(pat):
        return None, "Missing"

    if pat == 0:
        return None, "PAT Zero"

    ratio = cfo / pat

    if ratio > 1:
        label = "High Quality"
    elif ratio >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"

    return round(ratio, 2), label


# ---------------------------------
# CapEx Intensity
# ---------------------------------
def capex_intensity(capex, sales):
    if pd.isna(capex) or pd.isna(sales):
        return None, "Missing"

    if sales == 0:
        return None, "Sales Zero"

    intensity = abs(capex) / sales * 100

    if intensity < 3:
        label = "Asset Light"

    elif intensity <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(intensity, 2), label


# ---------------------------------
# FCF Conversion
# ---------------------------------
def fcf_conversion(fcf, operating_profit):
    if pd.isna(fcf) or pd.isna(operating_profit):
        return None

    if operating_profit == 0:
        return None

    return round(fcf / operating_profit * 100, 2)


# ---------------------------------
# Capital Allocation Pattern
# ---------------------------------
def capital_allocation(cfo, cfi, cff):

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = cfo_sign + cfi_sign + cff_sign

    mapping = {
        "+--": "Reinvestor",
        "++-": "Shareholder Returns",
        "+++": "Liquidating Assets",
        "-++": "Distress Signal",
        "--+": "Growth Funded by Debt",
        "+-+": "Mixed",
        "---": "Pre-Revenue",
        "-+-": "Other"
    }

    return pattern, mapping.get(pattern, "Unknown")