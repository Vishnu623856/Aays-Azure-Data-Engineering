from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    countDistinct,
    max,
    sum,
)


PROJECT_DIR = Path(__file__).resolve().parent.parent

SILVER_DIR = PROJECT_DIR / "output" / "silver" / "sales"
GOLD_DIR = PROJECT_DIR / "output" / "gold"


def create_spark_session():
    """Create a local Spark session."""

    return (
        SparkSession.builder
        .appName("AdventureWorksGoldAggregation")
        .master("local[*]")
        .getOrCreate()
    )


def load_silver(spark):
    """Load cleaned sales data from the Silver layer."""

    return spark.read.parquet(str(SILVER_DIR))


def create_monthly_sales(sales):
    """Create monthly sales performance dataset."""

    monthly_sales = (
        sales
        .groupBy(
            "OrderYear",
            "OrderMonth",
        )
        .agg(
            countDistinct("OrderNumber").alias("TotalOrders"),
            sum("OrderQuantity").alias("TotalQuantity"),
            sum("LineQuantity").alias("TotalLineQuantity"),
            avg("OrderQuantity").alias("AverageOrderQuantity"),
        )
        .orderBy(
            "OrderYear",
            "OrderMonth",
        )
    )

    return monthly_sales


def create_product_performance(sales):
    """Create product-level performance dataset."""

    product_performance = (
        sales
        .groupBy("ProductKey")
        .agg(
            countDistinct("OrderNumber").alias("TotalOrders"),
            sum("OrderQuantity").alias("TotalQuantity"),
            sum("LineQuantity").alias("TotalLineQuantity"),
            max("OrderDate").alias("LastOrderDate"),
        )
        .orderBy("ProductKey")
    )

    return product_performance


def write_gold(dataset, name):
    """Write a Gold dataset as Parquet."""

    output_path = GOLD_DIR / name

    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    (
        dataset.write
        .mode("overwrite")
        .parquet(str(output_path))
    )

    print(f"Gold dataset written to: {output_path}")


def main():
    """Run Gold aggregation pipeline."""

    print("Starting Gold aggregation...")

    spark = create_spark_session()

    try:
        sales = load_silver(spark)

        print(f"Silver records loaded: {sales.count():,}")

        print("\nCreating monthly sales performance...")

        monthly_sales = create_monthly_sales(sales)

        print("\nMonthly sales preview:")
        monthly_sales.show(10, truncate=False)

        write_gold(
            monthly_sales,
            "monthly_sales",
        )

        print("\nCreating product performance...")

        product_performance = create_product_performance(sales)

        print("\nProduct performance preview:")
        product_performance.show(10, truncate=False)

        write_gold(
            product_performance,
            "product_performance",
        )

        print("\nGold aggregation completed successfully.")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()