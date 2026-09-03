from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "Data"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def load_sales():
    files = [
        DATA_DIR / "AdventureWorks_Sales_2015.csv",
        DATA_DIR / "AdventureWorks_Sales_2016.csv",
        DATA_DIR / "AdventureWorks_Sales_2017.csv",
    ]

    sales = pd.concat(
        [pd.read_csv(file) for file in files],
        ignore_index=True
    )

    return sales


def transform_sales(sales):
    sales["OrderDate"] = pd.to_datetime(sales["OrderDate"])
    sales["StockDate"] = pd.to_datetime(sales["StockDate"])

    sales["OrderYear"] = sales["OrderDate"].dt.year
    sales["OrderMonth"] = sales["OrderDate"].dt.month

    sales["LineQuantity"] = (
        sales["OrderLineItem"] * sales["OrderQuantity"]
    )

    return sales


def validate_sales(sales):
    checks = {
        "No missing OrderNumber": sales["OrderNumber"].notna().all(),
        "No missing ProductKey": sales["ProductKey"].notna().all(),
        "No missing CustomerKey": sales["CustomerKey"].notna().all(),
        "All quantities positive": (sales["OrderQuantity"] > 0).all(),
    }

    print("\nDATA QUALITY RESULTS")
    print("-" * 40)

    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {check}")

    return all(checks.values())


def save_sales(sales):
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "sales_transformed.csv"

    sales.to_csv(output_file, index=False)

    print(f"\nTransformed data saved to: {output_file}")
    print(f"Output records: {len(sales):,}")


def main():
    print("Loading sales data...")

    sales = load_sales()

    print(f"Total sales records: {len(sales):,}")

    print("\nTransforming sales data...")

    sales = transform_sales(sales)

    if not validate_sales(sales):
        raise ValueError("Data quality validation failed.")

    save_sales(sales)

    print("\nETL pipeline completed successfully.")


if __name__ == "__main__":
    main()