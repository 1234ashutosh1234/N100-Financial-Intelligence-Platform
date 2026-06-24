import pandas as pd

data = {
    "Company": ["TCS", "Infosys", "Reliance", "HDFC Bank"],
    "Health_Score": [95, 92, 90, 88]
}

df = pd.DataFrame(data)

df = df.sort_values("Health_Score", ascending=False)

print(df)

df.to_csv("output/company_rankings.csv", index=False)

print("Ranking file created successfully!")