# Aays Azure Data Engineering Project

End-to-end Azure data engineering project based on the AdventureWorks sales dataset.
AdventureWorks CSV
       ↓
Azure Data Factory
       ↓
ADLS Gen2
       ↓
Bronze
       ↓
Databricks / PySpark
       ↓
Silver
       ↓
Gold
   ↙       ↘
Synapse    Streamlit
SQL        Dashboard
## Project Overview

This project demonstrates a complete data engineering workflow using Python, PySpark, Azure Data Factory, Azure Data Lake Storage Gen2, Azure Databricks, Azure Synapse Analytics, SQL, and Streamlit.

The pipeline ingests sales data, processes it through Bronze, Silver, and Gold layers, performs analytical queries, and presents the results through an interactive dashboard.

## Architecture

```text
AdventureWorks CSV
       |
       v
Azure Data Factory
       |
       v
Azure Data Lake Storage Gen2
       |
       +---------------------------+
       |                           |
       v                           |
Bronze Layer                       |
       |                           |
       v                           |
Silver Layer <--- Azure Databricks / PySpark
       |
       v
Gold Layer
       |
       +---------------------------+
       |                           |
       v                           v
Azure Synapse Serverless SQL   Streamlit Dashboard
       |                           |
       v                           v
SQL Analytics                Interactive Visuals
```

## Technologies Used

- Python
- SQL
- PySpark
- Pandas
- Azure Data Factory
- Azure Data Lake Storage Gen2
- Azure Databricks
- Azure Synapse Analytics
- Streamlit
- Plotly
- Parquet
- Git
- GitHub

## Data Pipeline

### 1. Source Data

The project uses the AdventureWorks sales dataset containing information about:

- Sales orders
- Customers
- Products
- Territories
- Product categories
- Returns

The sales data covers 2015, 2016, and 2017.

### 2. Bronze Layer

The Bronze layer stores ingested sales data in Parquet format with minimal transformation.

Azure Data Factory is used to demonstrate the ingestion process from source data into Azure Data Lake Storage Gen2.

### 3. Silver Layer

The Silver layer applies transformations using PySpark.

Transformations include:

- Converting `OrderDate` and `StockDate` to date types
- Extracting `OrderYear`
- Extracting `OrderMonth`
- Creating `LineQuantity`
- Performing data-quality validation

Data-quality checks include:

- Missing `OrderNumber`
- Missing `ProductKey`
- Missing `CustomerKey`
- Invalid dates
- Non-positive quantities

### 4. Gold Layer

The Gold layer contains analytical datasets designed for reporting and analysis.

#### Monthly Sales Performance

Contains:

- Order year
- Order month
- Total orders
- Total quantity
- Total line quantity
- Average order quantity

#### Product Performance

Contains:

- Product key
- Total orders
- Total quantity
- Total line quantity
- Last order date

## Azure Data Lake Storage Structure

```text
aays-data/
├── source/
│   └── sales/
├── bronze/
│   └── sales/
├── silver/
│   └── sales/
└── gold/
    ├── monthly_sales/
    └── product_performance/
```

## Azure Data Factory

Azure Data Factory is used as the ingestion/orchestration component.

The project includes a pipeline that demonstrates copying source sales data into the Bronze layer of Azure Data Lake Storage Gen2.

Main components include:

- `PL_Aays_Sales_ETL`
- `Copy_Sales_To_Bronze`
- `DS_Source_Sales_CSV`
- `DS_Bronze_Sales_Parquet`

## Azure Databricks

Azure Databricks is used for PySpark-based data transformation.

The Databricks workflow reads the Bronze Parquet data, performs transformations, validates the data, and writes the Silver and Gold datasets back to Azure Data Lake Storage Gen2.

The implementation uses secure Azure identity-based access rather than storing Azure credentials in the notebook.

## Azure Synapse Analytics

Azure Synapse Serverless SQL is used as the analytical SQL layer.

The Gold Parquet datasets are queried using `OPENROWSET`.

Example:

```sql
SELECT TOP 10
    *
FROM OPENROWSET(
    BULK 'https://aaysdataeng2026.dfs.core.windows.net/aays-data/gold/monthly_sales/*.parquet',
    FORMAT = 'PARQUET'
) AS [result];
```

Analytical queries include:

- Sales records by year
- Monthly sales performance
- Top products
- Top customers
- Sales by territory
- Overall sales summary

## SQL Analytics

The repository includes SQL queries for analyzing the transformed sales data.

Examples include:

### Sales by Year

```sql
SELECT
    OrderYear,
    COUNT(*) AS TotalSalesRecords,
    SUM(OrderQuantity) AS TotalQuantity
FROM silver_sales
GROUP BY OrderYear
ORDER BY OrderYear;
```

### Top Products

```sql
SELECT
    ProductKey,
    SUM(OrderQuantity) AS TotalQuantity,
    COUNT(DISTINCT OrderNumber) AS TotalOrders
FROM silver_sales
GROUP BY ProductKey
ORDER BY TotalQuantity DESC
LIMIT 10;
```

### Sales by Territory

```sql
SELECT
    TerritoryKey,
    COUNT(DISTINCT OrderNumber) AS TotalOrders,
    SUM(OrderQuantity) AS TotalQuantity
FROM silver_sales
GROUP BY TerritoryKey
ORDER BY TotalQuantity DESC;
```

## Data Warehouse Model

A star-schema-style analytical model is included in the project.

### Fact Table

```text
fact_sales
```

### Dimension Tables

```text
dim_customer
dim_product
dim_territory
dim_date
```

The model is designed to demonstrate dimensional modeling concepts used in analytical data warehouses.

## Data Quality

The PySpark pipeline performs data-quality validation before completing the transformation.

The local pipeline successfully processed:

```text
56,046 sales records
```

The following checks passed:

- No missing `OrderNumber`
- No missing `ProductKey`
- No missing `CustomerKey`
- All order quantities positive
- No invalid `OrderDate`
- No invalid `StockDate`

## Streamlit Dashboard

The project includes a local Streamlit dashboard built from the Gold-layer Parquet datasets.

The dashboard provides:

- Total orders
- Total quantity
- Product count
- Average quantity per order
- Monthly sales trend
- Top 10 products
- Monthly sales data
- Product performance data

### Run the Dashboard

Activate the Python virtual environment:

```bash
source .venv/bin/activate
```

Run:

```bash
streamlit run dashboard.py
```

Then open:

```text
http://localhost:8501
```

## Dashboard Preview

The dashboard provides an interactive view of the processed Gold-layer data, including monthly sales trends and top-performing products.

## Local Development

Create the Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install pandas pyspark jupyter streamlit plotly pyarrow
```

### Run the Local PySpark Pipeline

```bash
python src/pyspark_transform.py
```

### Run Bronze Ingestion

```bash
python src/bronze_ingestion.py
```

### Run Silver Transformation

```bash
python src/silver_transformation.py
```

### Run Gold Aggregation

```bash
python src/gold_aggregation.py
```

### Run the Dashboard

```bash
streamlit run dashboard.py
```

## Project Structure

```text
Aays-Azure-Data-Engineering/
│
├── Data/
│   ├── AdventureWorks_Sales_2015.csv
│   ├── AdventureWorks_Sales_2016.csv
│   ├── AdventureWorks_Sales_2017.csv
│   ├── AdventureWorks_Customers.csv
│   ├── AdventureWorks_Products.csv
│   └── ...
│
├── src/
│   ├── inspect_data.py
│   ├── transform_data.py
│   ├── pyspark_transform.py
│   ├── bronze_ingestion.py
│   ├── silver_transformation.py
│   ├── gold_aggregation.py
│   ├── analytics_queries.sql
│   └── create_warehouse.sql
│
├── dashboard.py
├── create_schema.sql
├── create_external_table.sql
├── create_views_servinglayer.sql
├── create_gold_views.sql
├── data_quality_checks.sql
├── query_insights.sql
├── data_transformations_databricks.ipynb
├── dataset_load.json
├── CHANGES.md
└── README.md
```

## Key Learning Areas

This project demonstrates practical experience with:

- ETL and ELT concepts
- Data ingestion
- Data transformation
- PySpark
- SQL analytics
- Data lake architecture
- Bronze/Silver/Gold data organization
- Data-quality validation
- Analytical data modeling
- Azure cloud services
- Serverless SQL
- Dashboard development
- Git version control

## Security

Azure credentials and secrets are not stored in the repository.

Azure authentication for the Databricks-to-ADLS connection uses Azure identity-based authentication rather than hard-coded credentials.

Sensitive credentials should always be stored using appropriate Azure secret-management or identity mechanisms.

## Cost Awareness

The Azure implementation was developed using Azure for Students resources.

The project uses Azure services such as:

- Azure Data Lake Storage Gen2
- Azure Data Factory
- Azure Databricks
- Azure Synapse Serverless SQL

Azure serverless services can incur usage-based charges, so unnecessary queries and compute usage should be avoided.

## Future Improvements

Possible future improvements include:

- Incremental data loading
- Parameterized Azure Data Factory pipelines
- Delta Lake tables
- Additional data-quality monitoring
- Automated pipeline scheduling
- More advanced dashboard filtering
- CI/CD integration
- Pipeline monitoring and alerting

## Author

**Vishnu Dutt**

Azure Data Engineering portfolio project focused on Python, SQL, PySpark, Azure data services, data pipelines, data warehousing, and analytical processing.