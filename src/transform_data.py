from pathlib import Path
import pandas as pd


DATA_DIR = Path(__file__).resolve().parent.parent / "Data"


def load_sales():
    """Load all yearly sales files into one dataframe."""

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
    """Clean and enrich the sales dataset."""

    sales["OrderDate"] = pd.to_datetime(sales["OrderDate"])
    sales["StockDate"] = pd.to_datetime(sales["StockDate"])

    sales["OrderYear"] = sales["OrderDate"].dt.year
    sales["OrderMonth"] = sales["OrderDate"].dt.month

    sales["LineQuantity"] = (
        sales["OrderLineItem"] * sales["OrderQuantity"]
    )

    return sales


def validate_sales(sales):
    """Run basic data-quality checks."""

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


def main():
    print("Loading sales data...")

    sales = load_sales()

    print(f"Total sales records: {len(sales):,}")

    sales = transform_sales(sales)

    if not validate_sales(sales):
        raise ValueError("Data quality validation failed.")

    print("\nTransformation completed successfully.")

    print("\nSample transformed data:")
    print(
        sales[
            [
                "OrderNumber",
                "OrderDate",
                "ProductKey",
                "CustomerKey",
                "OrderQuantity",
                "OrderYear",
                "OrderMonth",
                "LineQuantity",
            ]
        ].head()
    )


if __name__ == "__main__":
    main()