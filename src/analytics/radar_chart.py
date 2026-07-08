"""
N100 Financial Intelligence Platform
Sprint 3
Radar Chart Generator
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

DB = "data/nifty100.db"


class RadarChartEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB)

        self.df = pd.read_sql("""
        SELECT *
        FROM financial_ratios
        """, self.conn)

        os.makedirs("reports/radar_charts", exist_ok=True)

    # ------------------------------------------------

    def generate(self):

        metrics = [

            "return_on_equity_pct",

            "roce_pct",

            "net_profit_margin_pct",

            "asset_turnover",

            "financial_health_score"

        ]

        companies = self.df["company_id"].unique()[:20]

        for company in companies:

            data = self.df[
                self.df["company_id"] == company
            ].iloc[-1]

            values = []

            for m in metrics:

                values.append(float(data[m]))

            values += values[:1]

            angles = np.linspace(
                0,
                2*np.pi,
                len(metrics),
                endpoint=False
            ).tolist()

            angles += angles[:1]

            plt.figure(figsize=(6,6))

            ax = plt.subplot(111, polar=True)

            ax.plot(
                angles,
                values,
                linewidth=2
            )

            ax.fill(
                angles,
                values,
                alpha=0.25
            )

            ax.set_xticks(angles[:-1])

            ax.set_xticklabels(metrics)

            plt.title(company)

            plt.savefig(
                f"reports/radar_charts/{company}_radar.png"
            )

            plt.close()

        print("✓ Radar charts generated")

        self.conn.close()


if __name__ == "__main__":

    engine = RadarChartEngine()

    engine.generate()