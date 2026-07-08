"""
N100 Financial Intelligence Platform
Sprint 3
Financial Screener Engine
"""

import sqlite3
import pandas as pd
import yaml

DB = "data/nifty100.db"
CONFIG = "config/screener_config.yaml"


class ScreenerEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB)

        with open(CONFIG, "r") as f:
            self.config = yaml.safe_load(f)

        print("=" * 60)
        print("Financial Screener Engine")
        print("=" * 60)

        self.load_data()

    # -------------------------------------------------

    def load_data(self):

        self.ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        self.market = pd.read_sql(
            "SELECT * FROM market_cap",
            self.conn
        )

        print("Financial Ratios :", len(self.ratios))
        print("Market Cap       :", len(self.market))

    # -------------------------------------------------

    def merge_tables(self):

        print("\nMerging Tables...")

        self.ratios["company_id"] = self.ratios["company_id"].astype(str)
        self.market["company_id"] = self.market["company_id"].astype(str)

        self.ratios["year"] = (
            self.ratios["year"]
            .astype(str)
            .str.extract(r"(\d{4})")
        )

        self.market["year"] = self.market["year"].astype(str)

        self.df = pd.merge(
            self.ratios,
            self.market,
            on=["company_id", "year"],
            how="left"
        )

        print("Rows :", len(self.df))
        print("Columns :", len(self.df.columns))

        print("\nPreview")
        print(self.df.head())

    # -------------------------------------------------

    def quality_compounder(self):

        print("\n" + "=" * 60)
        print("Quality Compounder")
        print("=" * 60)

        cfg = self.config["quality_compounder"]

        self.quality_df = (
    self.df[
        (self.df["return_on_equity_pct"] >= cfg["roe_min"]) &
        (self.df["roce_pct"] >= cfg["roce_min"]) &
        (self.df["debt_to_equity"] <= cfg["debt_to_equity_max"]) &
        (self.df["free_cash_flow_cr"] >= cfg["free_cash_flow_min"]) &
        (self.df["sales_cagr_pct"] >= cfg["sales_cagr_min"])
    ]
    .sort_values(
        by="composite_quality_score",
        ascending=False
    )
    .copy()
)

        print("Companies :", len(self.quality_df))

    # -------------------------------------------------

    def value_pick(self):

        cfg = self.config["value_pick"]

        self.value_df = self.df[
            (self.df["pe_ratio"] <= cfg["pe_max"]) &
            (self.df["pb_ratio"] <= cfg["pb_max"]) &
            (self.df["debt_to_equity"] <= cfg["debt_to_equity_max"]) &
            (self.df["dividend_yield_pct"] >= cfg["dividend_yield_min"])
        ].copy()

        print("Value Pick :", len(self.value_df))

    # -------------------------------------------------

    def growth_accelerator(self):

        cfg = self.config["growth_accelerator"]

        self.growth_df = self.df[
            (self.df["profit_cagr_pct"] >= cfg["profit_cagr_min"]) &
            (self.df["sales_cagr_pct"] >= cfg["sales_cagr_min"]) &
            (self.df["debt_to_equity"] <= cfg["debt_to_equity_max"])
        ].copy()

        print("Growth Accelerator :", len(self.growth_df))

    # -------------------------------------------------

    def dividend_champion(self):

        cfg = self.config["dividend_champion"]

        self.dividend_df = self.df[
            (self.df["dividend_yield_pct"] >= cfg["dividend_yield_min"]) &
            (self.df["free_cash_flow_cr"] >= cfg["free_cash_flow_min"])
        ].copy()

        print("Dividend Champion :", len(self.dividend_df))

    # -------------------------------------------------

    def debt_free_bluechip(self):

        cfg = self.config["debt_free_bluechip"]

        self.debtfree_df = self.df[
            (self.df["debt_to_equity"] <= cfg["debt_to_equity_max"]) &
            (self.df["return_on_equity_pct"] >= cfg["roe_min"]) &
            (self.df["market_cap_crore"] >= cfg["market_cap_min"])
        ].copy()

        print("Debt Free Blue Chip :", len(self.debtfree_df))

    # -------------------------------------------------

    def turnaround_watch(self):

        cfg = self.config["turnaround_watch"]

        self.turnaround_df = self.df[
            (self.df["sales_cagr_pct"] >= cfg["sales_cagr_min"]) &
            (self.df["free_cash_flow_cr"] >= cfg["free_cash_flow_min"])
        ].copy()

        print("Turnaround Watch :", len(self.turnaround_df))

    # -------------------------------------------------
    # -------------------------------------------------
    # Composite Quality Score
    # -------------------------------------------------

    def calculate_composite_score(self):

        print("\n" + "=" * 60)
        print("Calculating Composite Score")
        print("=" * 60)

        self.df["composite_quality_score"] = (
            self.df["financial_health_score"].fillna(0) * 20
            + self.df["growth_score"].fillna(0) * 20
            + self.df["return_on_equity_pct"].fillna(0) * 0.8
            + self.df["roce_pct"].fillna(0) * 0.8
            + self.df["net_profit_margin_pct"].fillna(0) * 0.4
        ).round(2)

        print("✓ Composite Score Calculated")

        print(
            self.df[
                [
                    "company_id",
                    "year",
                    "composite_quality_score"
                ]
            ].head()
        )
    def close(self):

        self.conn.close()

        print("\nDatabase Closed")

        # ==================================================
# Export Screeners
# ==================================================

def export_screeners(engine):

    print("\n" + "=" * 60)
    print("Exporting Screeners")
    print("=" * 60)

    output_file = "output/screener_output.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

        engine.quality_df.to_excel(
            writer,
            sheet_name="Quality Compounder",
            index=False
        )

        engine.value_df.to_excel(
            writer,
            sheet_name="Value Pick",
            index=False
        )

        engine.growth_df.to_excel(
            writer,
            sheet_name="Growth Accelerator",
            index=False
        )

        engine.dividend_df.to_excel(
            writer,
            sheet_name="Dividend Champion",
            index=False
        )

        engine.debtfree_df.to_excel(
            writer,
            sheet_name="Debt Free Blue Chip",
            index=False
        )

        engine.turnaround_df.to_excel(
            writer,
            sheet_name="Turnaround Watch",
            index=False
        )

    print("✓ Screener exported successfully")
    print("Saved to :", output_file)


# ==================================================
# Main
# ==================================================

if __name__ == "__main__":

    engine = ScreenerEngine()
engine.merge_tables()

engine.calculate_composite_score()

engine.quality_compounder()

engine.value_pick()

engine.growth_accelerator()

engine.dividend_champion()

engine.debt_free_bluechip()

engine.turnaround_watch()

export_screeners(engine)

engine.close()