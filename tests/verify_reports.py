from pathlib import Path

tearsheets = len(list(Path("reports/tearsheets").glob("*.pdf")))
sector = len(list(Path("reports/sector").glob("*.pdf")))
portfolio = len(list(Path("reports/portfolio").glob("*.pdf")))

print("Tearsheets :", tearsheets)
print("Sector PDFs :", sector)
print("Portfolio PDFs :", portfolio)