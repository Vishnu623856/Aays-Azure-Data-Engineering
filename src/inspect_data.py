import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "Data"

for file in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(file, encoding="latin1")

    print("\n" + "=" * 60)
    print(f"FILE: {file.name}")
    print("=" * 60)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    print(list(df.columns))

    print("\nFirst 3 rows:")
    print(df.head(3))