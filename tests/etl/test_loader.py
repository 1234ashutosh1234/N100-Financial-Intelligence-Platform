import pandas as pd

def test_companies_file():

    df = pd.read_excel(
        "data/raw/companies.xlsx"
    )

    assert len(df) > 0