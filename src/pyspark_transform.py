from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, to_date


# Project directories
DATA_DIR = Path(__file__).resolve().parent.parent / "Data"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def create_spark_session():
    """Create a local Spark session for development and testing."""
    return (
        SparkSession.builder
        .appName("AdventureWorksSalesETL")
        .master("local[*]")
        .getOrCreate()
    )


def load_sales(spark):
    """Load sales data from the three yearly CSV files."""

    files = [
        str(DATA_DIR / "AdventureWorks_Sales_2015.csv"),
        str(DATA_DIR / "AdventureWorks_Sales_2016.csv"),
        str(DATA_DIR / "AdventureWorks_Sales_2017.csv"),
    ]

    sales = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(files)
    )

    return sales


def transform_sales(sales):
    """Clean and transform the sales dataset."""

    sales = (
        sales
        # Convert source date strings into Spark date values.
        # Source format is M/d/yyyy, e.g. 1/1/2017.
        .withColumn(
            "OrderDate",
            to_date(col("OrderDate"), "M/d/yyyy")
        )
        .withColumn(
            "StockDate",
            to_date(col("StockDate"), "M/d/yyyy")
        )

        # Create useful date attributes
        .withColumn(
            "OrderYear",
            year("OrderDate")
        )
        .withColumn(
            "OrderMonth",
            month("OrderDate")
        )

        # Create calculated quantity field
        .withColumn(
            "LineQuantity",
            col("OrderLineItem") * col("OrderQuantity")
        )
    )

    return sales


def validate_sales(sales):
    """Run basic data-quality checks."""

    checks = {
        "No missing OrderNumber": sales.filter(
            col("OrderNumber").isNull()
        ).count() == 0,

        "No missing ProductKey": sales.filter(
            col("ProductKey").isNull()
        ).count() == 0,

        "No missing CustomerKey": sales.filter(
            col("CustomerKey").isNull()
        ).count() == 0,

        "All quantities positive": sales.filter(
            col("OrderQuantity") <= 0
        ).count() == 0,

        "No invalid OrderDate": sales.filter(
            col("OrderDate").isNull()
        ).count() == 0,

        "No invalid StockDate": sales.filter(
            col("StockDate").isNull()
        ).count() == 0,
    }

    print("\nDATA QUALITY RESULTS")
    print("-" * 40)

    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {check}")

    return all(checks.values())


def save_sales(sales):
    """Save transformed sales data as Parquet."""

    output_path = OUTPUT_DIR / "sales_pyspark"

    OUTPUT_DIR.mkdir(exist_ok=True)

    (
        sales.write
        .mode("overwrite")
        .parquet(str(output_path))
    )

    print(f"\nPySpark output saved to: {output_path}")


def main():
    """Run the complete PySpark ETL pipeline."""

    print("Starting PySpark sales ETL...")

    spark = create_spark_session()

    try:
        # Extract
        sales = load_sales(spark)

        print(f"Total sales records: {sales.count():,}")

        # Transform
        print("\nTransforming sales data...")

        sales = transform_sales(sales)

        # Validate
        if not validate_sales(sales):
            raise ValueError("Data quality validation failed.")

        # Preview
        print("\nSample transformed data:")

        sales.select(
            "OrderNumber",
            "OrderDate",
            "ProductKey",
            "CustomerKey",
            "OrderQuantity",
            "OrderYear",
            "OrderMonth",
            "LineQuantity",
        ).show(5, truncate=False)

        # Load
        save_sales(sales)

        print("\nPySpark ETL pipeline completed successfully.")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()