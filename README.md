# Azure Retail Data Engineering Pipeline

## Overview
An end-to-end Azure data engineering project using the AdventureWorks retail dataset. The solution demonstrates ingestion, distributed transformation, data-quality validation, analytics-ready serving datasets, SQL warehousing, and Power BI reporting.

## Architecture

```text
AdventureWorks CSV
      |
      v
Azure Data Factory
      |
      v
ADLS Gen2 - Raw
      |
      v
Azure Databricks / PySpark
      |
      +--> Data quality checks
      |
      +--> ADLS Gen2 - Transform (Parquet)
      |
      +--> ADLS Gen2 - Serving (Gold metrics)
      |
      v
Azure Synapse Serverless SQL
      |
      v
Power BI
```

## What I changed / added
- Parameterized the Databricks storage-account configuration instead of embedding cloud credentials.
- Removed committed client secrets from the notebook.
- Added reusable PySpark data-quality checks for null keys, positive quantities, and duplicate identifiers.
- Added analytics-ready Gold datasets for monthly sales performance and product return performance.
- Made transformation writes idempotent with overwrite mode, preventing duplicate output on repeated runs.
- Added Synapse data-quality SQL checks for nulls, invalid quantities, duplicates, and orphan product keys.
- Added business-focused SQL views and KPI examples.
- Corrected a customer-view reference in the original insight queries.

## Azure components
- Azure Data Factory — ingestion and orchestration
- Azure Data Lake Storage Gen2 — raw, transform, and serving zones
- Azure Databricks — PySpark transformation and validation
- Azure Synapse Analytics — serverless SQL / warehouse-style serving
- Power BI — analytics and visualization

## Data layers

### Raw
Source CSV files are retained with minimal modification.

### Transform
Databricks converts source data into analytics-friendly Parquet datasets, including type normalization and derived fields.

### Serving / Gold
Business-oriented datasets are created for downstream SQL and BI:
- Monthly sales performance
- Product return performance

## Data quality
The Databricks notebook validates:
- Required sales identifiers are not null
- Order quantities are positive
- Sales order numbers are unique
- Customer keys are unique
- Product keys are unique

Additional Synapse SQL checks are provided in `data_quality_checks.sql`.

## Running the Databricks notebook
1. Upload the notebook to Azure Databricks.
2. Configure an Azure Key Vault-backed secret scope or managed identity for ADLS access.
3. Set the `storage_account` notebook parameter.
4. Run the notebook.
5. Execute the Synapse SQL scripts after the Parquet outputs are available.
6. Repoint the Power BI dataset to your Synapse endpoint if required.

## Security note
No Azure client secrets, tenant secrets, or access tokens are included in this repository. Authentication should be supplied through managed identity or a Databricks secret scope.

## Repository structure
```text
Data/                              # AdventureWorks source data
data_transformations_databricks.ipynb
dataset_load.json
create_schema.sql
create_views_servinglayer.sql
create_external_table.sql
create_gold_views.sql
data_quality_checks.sql
query_insights.sql
Azure_PowerBI_Dashboard.pbix
README.md
```
