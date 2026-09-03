
CREATE DATABASE SCOPED CREDENTIAL cred_adls_managed_identity
WITH
IDENTITY = 'Managed Identity'

CREATE EXTERNAL DATA SOURCE source_transform
WITH
(
    LOCATION = 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/transform/',
    CREDENTIAL = cred_adls_managed_identity
)

CREATE EXTERNAL DATA SOURCE source_serving
WITH
(
    LOCATION = 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/serving/',
    CREDENTIAL = cred_adls_managed_identity
)

CREATE EXTERNAL FILE FORMAT format_parquet
WITH
(
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
    
)

CREATE EXTERNAL TABLE ServingLayer.ext_sales
WITH
(
    LOCATION = 'ext_sales',
    DATA_SOURCE = source_serving,
    FILE_FORMAT = format_parquet

)
AS
SELECT *
FROM ServingLayer.Sales

