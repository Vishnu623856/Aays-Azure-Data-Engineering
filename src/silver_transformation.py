from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, month, to_date, year


PROJECT_DIR = Path(__file__).resolve().parent.parent

BRONZE_DIR = PROJECT_DIR / "output" / "bronze" / "sales"
SILVER_DIR = PROJECT_DIR / "output" / "silver"


def create_spark_session():
    """Create a local Spark session."""
    return (
        SparkSession.builder
        .appName("AdventureWorksSilverTransformation")
        .master("local[*]")
        .getOrCreate()
    )


def load_bronze(spark):
    """Load sales data from the Bronze layer."""

    sales = spark.read.parquet(str(BRONZE_DIR))

    return sales


def transform_sales(sales):
    """Clean and standardize Bronze sales data."""

    sales = (
        sales
        # Convert source date strings into Spark date values.
        .withColumn(
            "OrderDate",
            to_date(col("OrderDate"), "M/d/yyyy")
        )
        .withColumn(
            "StockDate",
            to_date(col("StockDate"), "M/d/yyyy")
        )

        # Add useful date attributes.
        .withColumn(
            "OrderYear",
            year("OrderDate")
        )
        .withColumn(
            "OrderMonth",
            month("OrderDate")
        )

        # Calculate line quantity.
        .withColumn(
            "LineQuantity",
            col("OrderLineItem") * col("OrderQuantity")
        )
    )

    return sales


def validate_sales(sales):
    """Run Silver-layer data-quality checks."""

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

    print("\nSILVER DATA QUALITY RESULTS")
    print("-" * 40)

    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {check}")

    return all(checks.values())


def write_silver(sales):
    """Write cleaned sales data to the Silver layer."""

    output_path = SILVER_DIR / "sales"

    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    (
        sales.write
        .mode("overwrite")
        .parquet(str(output_path))
    )

    print(f"\nSilver data written to: {output_path}")


def main():
    """Run the complete Silver transformation pipeline."""

    print("Starting Silver transformation...")

    spark = create_spark_session()

    try:
        # Read Bronze data.
        sales = load_bronze(spark)

        print(f"Bronze records loaded: {sales.count():,}")

        # Transform.
        print("\nTransforming Bronze data...")

        sales = transform_sales(sales)

        # Validate.
        if not validate_sales(sales):
            raise ValueError("Silver data-quality validation failed.")

        # Display schema.
        print("\nSilver schema:")
        sales.printSchema()

        # Preview.
        print("\nSample Silver data:")

        sales.select(
            "OrderNumber",
            "OrderDate",
            "StockDate",
            "ProductKey",
            "CustomerKey",
            "OrderQuantity",
            "OrderYear",
            "OrderMonth",
            "LineQuantity",
        ).show(5, truncate=False)

        # Write Silver.
        write_silver(sales)

        print("\nSilver transformation completed successfully.")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()