"""
N100 Financial Intelligence Platform
Sprint 6
KMeans Clustering
"""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

DB = "data/nifty100.db"

OUTPUT = Path("output")
REPORTS = Path("reports")

OUTPUT.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)


class ClusterEngine:

    def __init__(self):

        print("=" * 60)
        print("KMeans Clustering Engine")
        print("=" * 60)

        self.conn = sqlite3.connect(DB)

    # --------------------------------------------------

    def load_data(self):

        self.df = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                return_on_equity_pct,
                debt_to_equity,
                sales_cagr_pct,
                free_cash_flow_cr,
                operating_profit_margin_pct
            FROM financial_ratios
            """,
            self.conn
        )

        print("Rows Loaded :", len(self.df))

    # --------------------------------------------------

    def preprocess(self):

        latest = (
            self.df
            .sort_values("year")
            .groupby("company_id")
            .tail(1)
            .reset_index(drop=True)
        )

        self.company_ids = latest["company_id"]

        X = latest.drop(columns=["company_id", "year"])

        imputer = SimpleImputer(strategy="median")
        X = imputer.fit_transform(X)

        scaler = StandardScaler()
        self.X = scaler.fit_transform(X)

    # --------------------------------------------------

    def elbow_plot(self):

        inertia = []

        for k in range(2, 11):

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10
            )

            model.fit(self.X)

            inertia.append(model.inertia_)

        plt.figure(figsize=(7,5))
        plt.plot(range(2,11), inertia, marker="o")
        plt.title("Elbow Method")
        plt.xlabel("Clusters")
        plt.ylabel("Inertia")
        plt.grid(True)

        plt.savefig(REPORTS / "elbow_plot.png")
        plt.close()

    # --------------------------------------------------

    def cluster(self):

        model = KMeans(
            n_clusters=5,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(self.X)

        names = {
            0: "High Quality",
            1: "Growth",
            2: "Value",
            3: "Turnaround",
            4: "Balanced"
        }

        output = pd.DataFrame({

            "company_id": self.company_ids,

            "cluster_id": labels,

            "cluster_name": [
                names[i] for i in labels
            ]

        })

        output.to_csv(
            OUTPUT / "cluster_labels.csv",
            index=False
        )

        print()
        print("✓ cluster_labels.csv created")

    # --------------------------------------------------

    def close(self):

        self.conn.close()

        print("\nDatabase Closed")


if __name__ == "__main__":

    app = ClusterEngine()

    app.load_data()

    app.preprocess()

    app.elbow_plot()

    app.cluster()

    app.close()