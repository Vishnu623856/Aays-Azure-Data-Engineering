-- Create view Calender
CREATE VIEW ServingLayer.Calender
AS
SELECT * 
FROM
OPENROWSET(
    BULK 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/transform/Calender/',
    FORMAT = 'PARQUET' 
) AS QUERY1

--Create view Customer
CREATE VIEW ServingLayer.Customers_det
AS
SELECT * 
FROM
OPENROWSET(
    BULK 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/transform/Customers/part-00000-tid-8669070808659561250-c991e217-b8b8-462d-ac3e-f3a0e228d653-26-1-c000.snappy.parquet',
    FORMAT = 'PARQUET' 
) AS QUERY2

-- Create view Product_Subcategories
CREATE VIEW ServingLayer.Product_Subcategories
AS
SELECT * 
FROM
OPENROWSET(
    BULK 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/transform/Product_Subcategories/',
    FORMAT = 'PARQUET' 
) AS QUERY3

-- Create view Products
CREATE VIEW ServingLayer.Products
AS
SELECT * 
FROM
OPENROWSET(
    BULK 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/transform/Products/',
    FORMAT = 'PARQUET' 
) AS QUERY4

-- Create view Returns
CREATE VIEW ServingLayer.Returns
AS
SELECT * 
FROM
OPENROWSET(
    BULK 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/transform/Returns/',
    FORMAT = 'PARQUET' 
) AS QUERY5

-- Create view Sales
CREATE VIEW ServingLayer.Sales
AS
SELECT * 
FROM
OPENROWSET(
    BULK 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/transform/Sales/',
    FORMAT = 'PARQUET' 
) AS QUERY6

-- Create view Territories
CREATE VIEW ServingLayer.Territories
AS
SELECT * 
FROM
OPENROWSET(
    BULK 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/transform/Territories/',
    FORMAT = 'PARQUET' 
) AS QUERY7

-- Create view Product Categories
CREATE VIEW ServingLayer.Products_Categories
AS
SELECT * 
FROM
OPENROWSET(
    BULK 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/transform/Products_Categories/',
    FORMAT = 'PARQUET' 
) AS QUERY8