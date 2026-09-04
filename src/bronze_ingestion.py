from pathlib import Path

from pyspark.sql import SparkSession


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "Data"
BRONZE_DIR = PROJECT_DIR / "output" / "bronze"


def create_spark_session():
    """Create a local Spark session."""
    return (
        SparkSession.builder
        .appName("AdventureWorksBronzeIngestion")
        .master("local[*]")
        .getOrCreate()
    )


def load_raw_sales(spark):
    """Load the original yearly sales CSV files."""

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


def write_bronze(sales):
    """Write raw sales data to the Bronze layer."""

    output_path = BRONZE_DIR / "sales"

    BRONZE_DIR.mkdir(parents=True, exist_ok=True)

    (
        sales.write
        .mode("overwrite")
        .parquet(str(output_path))
    )

    print(f"\nBronze data written to: {output_path}")


def main():
    """Run Bronze ingestion."""

    print("Starting Bronze ingestion...")

    spark = create_spark_session()

    try:
        sales = load_raw_sales(spark)

        record_count = sales.count()

        print(f"Raw sales records loaded: {record_count:,}")

        print("\nBronze schema:")
        sales.printSchema()

        write_bronze(sales)

        print("\nBronze ingestion completed successfully.")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
    