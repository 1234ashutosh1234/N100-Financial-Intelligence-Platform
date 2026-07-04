"""
N100 Financial Intelligence Platform
Sprint 2 - Financial Ratio Engine
Part 1 - Database Loading
"""

import sqlite3
import pandas as pd
import numpy as np

DB = "data/nifty100.db"


class RatioEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB)

        self.profit = None
        self.balance = None
        self.cash = None
        self.market = None
        self.analysis = None

        self.df = None

    # ===================================================
    # Load Tables
    # ===================================================

    def load_tables(self):

        print("=" * 60)
        print("Loading Database Tables")
        print("=" * 60)

        self.profit = pd.read_sql(
            "SELECT * FROM profitandloss",
            self.conn
        )

        self.balance = pd.read_sql(
            "SELECT * FROM balancesheet",
            self.conn
        )

        self.cash = pd.read_sql(
            "SELECT * FROM cashflow",
            self.conn
        )

        self.market = pd.read_sql(
            "SELECT * FROM market_cap",
            self.conn
        )

        self.analysis = pd.read_sql(
            "SELECT * FROM analysis",
            self.conn
        )

        print(f"Profit & Loss : {len(self.profit)}")
        print(f"Balance Sheet : {len(self.balance)}")
        print(f"Cash Flow     : {len(self.cash)}")
        print(f"Market Cap    : {len(self.market)}")
        print(f"Analysis      : {len(self.analysis)}")

        # Remove duplicate company-year rows
        self.profit = self.profit.drop_duplicates(
            subset=["company_id", "year"]
        )

        self.balance = self.balance.drop_duplicates(
            subset=["company_id", "year"]
        )

        self.cash = self.cash.drop_duplicates(
            subset=["company_id", "year"]
        )

        # Convert merge keys
        for table in [self.profit, self.balance, self.cash]:

            table["company_id"] = table["company_id"].astype(str)
            table["year"] = table["year"].astype(str)

        self.market["company_id"] = self.market["company_id"].astype(str)

        self.market["year"] = (
            self.market["year"]
            .astype(str)
            .apply(lambda x: f"Mar {x}")
        )

        self.analysis["company_id"] = (
            self.analysis["company_id"]
            .astype(str)
        )

        print("\nTables Loaded Successfully")

            # ===================================================
    # Merge Tables
    # ===================================================

    def merge_tables(self):

        print("\n" + "=" * 60)
        print("Merging Financial Tables")
        print("=" * 60)

        # -------------------------------
        # Profit + Balance
        # -------------------------------

        self.df = pd.merge(
            self.profit,
            self.balance,
            on=["company_id", "year"],
            how="inner",
            suffixes=("_pl", "_bs")
        )

        print("✓ Profit + Balance :", self.df.shape)

        # -------------------------------
        # + Cash Flow
        # -------------------------------

        self.df = pd.merge(
            self.df,
            self.cash,
            on=["company_id", "year"],
            how="inner"
        )

        print("✓ + Cash Flow      :", self.df.shape)

        # -------------------------------
        # Market Cap
        # -------------------------------

        market_cols = [
            "company_id",
            "year",
            "market_cap_crore",
            "enterprise_value_crore",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "dividend_yield_pct"
        ]

        market = self.market[market_cols]

        self.df = pd.merge(
            self.df,
            market,
            on=["company_id", "year"],
            how="left"
        )

        print("✓ + Market Cap     :", self.df.shape)

        # -------------------------------
        # Analysis
        # -------------------------------

        analysis_cols = [
            "company_id",
            "compounded_sales_growth",
            "compounded_profit_growth",
            "stock_price_cagr",
            "roe"
        ]

        analysis = self.analysis[analysis_cols]

        self.df = pd.merge(
            self.df,
            analysis,
            on="company_id",
            how="left"
        )

        print("✓ + Analysis       :", self.df.shape)

        print("\nMerge Completed Successfully")
        print(f"Rows    : {len(self.df)}")
        print(f"Columns : {len(self.df.columns)}")

        print("\nPreview:\n")
     

            # ===================================================
    # Financial Ratio Calculation
    # ===================================================

    def calculate_ratios(self):

        print("\n" + "=" * 60)
        print("Calculating Financial Ratios")
        print("=" * 60)

        # Net Profit Margin
        self.df["net_profit_margin_pct"] = (
            self.df["net_profit"] /
            self.df["sales"] * 100
        ).round(2)

        # Operating Profit Margin
        self.df["operating_profit_margin_pct"] = (
            self.df["operating_profit"] /
            self.df["sales"] * 100
        ).round(2)

        # Return on Equity
        equity = (
            self.df["equity_capital"] +
            self.df["reserves"]
        )

        self.df["return_on_equity_pct"] = np.where(
            equity == 0,
            np.nan,
            (
                self.df["net_profit"] /
                equity * 100
            ).round(2)
        )

        # Debt to Equity
        self.df["debt_to_equity"] = np.where(
            equity == 0,
            np.nan,
            (
                self.df["borrowings"] /
                equity
            ).round(2)
        )

        # Interest Coverage
        self.df["interest_coverage"] = np.where(
            self.df["interest"] == 0,
            np.nan,
            (
                (
                    self.df["operating_profit"] +
                    self.df["other_income"]
                )
                /
                self.df["interest"]
            ).round(2)
        )

        # Asset Turnover
        self.df["asset_turnover"] = np.where(
            self.df["total_assets"] == 0,
            np.nan,
            (
                self.df["sales"] /
                self.df["total_assets"]
            ).round(2)
        )

        # Free Cash Flow
        self.df["free_cash_flow_cr"] = (
            self.df["operating_activity"] +
            self.df["investing_activity"]
        ).round(2)

                # ===================================================
        # ROCE (Return on Capital Employed)
        # ===================================================

        capital_employed = (
            self.df["equity_capital"] +
            self.df["reserves"] +
            self.df["borrowings"]
        )

        self.df["roce_pct"] = np.where(
            capital_employed == 0,
            np.nan,
            (
                self.df["operating_profit"] /
                capital_employed * 100
            ).round(2)
        )

        # ===================================================
        # ROA (Return on Assets)
        # ===================================================

        self.df["roa_pct"] = np.where(
            self.df["total_assets"] == 0,
            np.nan,
            (
                self.df["net_profit"] /
                self.df["total_assets"] * 100
            ).round(2)
        )

        # ===================================================
        # Financial Health Score
        # ===================================================

        score = pd.Series(0, index=self.df.index)

        score += (self.df["return_on_equity_pct"] > 15).astype(int)
        score += (self.df["net_profit_margin_pct"] > 10).astype(int)
        score += (self.df["debt_to_equity"] < 1).astype(int)
        score += (self.df["interest_coverage"] > 3).fillna(False).astype(int)
        score += (self.df["free_cash_flow_cr"] > 0).astype(int)

        self.df["financial_health_score"] = score

        print("✓ Financial Ratios Calculated")

        print("\nPreview\n")

        print(
       self.df[
        [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "return_on_equity_pct",
            "roce_pct",
            "roa_pct",
            "financial_health_score"
        ]
    ].head()
)

            # ===================================================
    # Close Database
    # ===================================================

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")

            # ===================================================
    # Save Financial Ratios
    # ===================================================


    # ===================================================
    # Growth Analytics
    # ===================================================

    def calculate_growth(self):

        print("\n" + "=" * 60)
        print("Calculating Growth Analytics")
        print("=" * 60)

        # Sort company records
        self.df = self.df.sort_values(
            ["company_id", "year"]
        )

        # Sales CAGR (%)
        self.df["sales_cagr_pct"] = (
            self.df.groupby("company_id")["sales"]
            .pct_change() * 100
        ).round(2)

        # Net Profit CAGR (%)
        self.df["profit_cagr_pct"] = (
            self.df.groupby("company_id")["net_profit"]
            .pct_change() * 100
        ).round(2)

        # EPS CAGR (%)
        self.df["eps_cagr_pct"] = (
            self.df.groupby("company_id")["eps"]
            .pct_change() * 100
        ).round(2)

        # Growth Score
        score = pd.Series(0, index=self.df.index)

        score += (self.df["sales_cagr_pct"] > 10).fillna(False).astype(int)
        score += (self.df["profit_cagr_pct"] > 10).fillna(False).astype(int)
        score += (self.df["eps_cagr_pct"] > 10).fillna(False).astype(int)

        self.df["growth_score"] = score

        print("✓ Growth Analytics Calculated")

        print("\nGrowth Columns Created:")

        print(
              self.df[
        [
            "sales_cagr_pct",
            "profit_cagr_pct",
            "eps_cagr_pct",
            "growth_score"
        ]
    ].head()
)

        print(
            self.df[
                [
                    "company_id",
                    "year",
                    "sales_cagr_pct",
                    "profit_cagr_pct",
                    "eps_cagr_pct",
                    "growth_score"
                ]
            ].head()
        )


    def save_ratios(self):

        print("\n" + "=" * 60)
        print("Saving Financial Ratios")
        print("=" * 60)
        print("\nColumns Available:")
        
        ratios = self.df[
            [
                "company_id",
                "year",

                "net_profit_margin_pct",
                "operating_profit_margin_pct",
                "return_on_equity_pct",
                "debt_to_equity",
                "interest_coverage",
                "asset_turnover",
                "free_cash_flow_cr",

                "roce_pct",
                "roa_pct",
                "financial_health_score",

                "sales_cagr_pct",
                "profit_cagr_pct",
                "eps_cagr_pct",
                "growth_score"
            ]
        ].copy()
        ratios.to_sql(
            "financial_ratios",
            self.conn,
            if_exists="replace",
            index=False
        )

        

        print("✓ financial_ratios table saved successfully")
        print(f"Rows Saved : {len(ratios)}")


# ===================================================
# Main
# ===================================================

if __name__ == "__main__":

    engine = RatioEngine()

    engine.load_tables()

    engine.merge_tables()

    engine.calculate_ratios()

    engine.calculate_growth()

    engine.save_ratios()

    engine.close()