-- Analytics-ready views for the serving layer.
-- Replace the storage account placeholder with your ADLS Gen2 account.

CREATE OR ALTER VIEW ServingLayer.MonthlySalesPerformance
AS
SELECT *
FROM OPENROWSET(
    BULK 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/serving/Gold_MonthlySales/',
    FORMAT = 'PARQUET'
) AS rows;

CREATE OR ALTER VIEW ServingLayer.ProductReturnPerformance
AS
SELECT *
FROM OPENROWSET(
    BULK 'https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/serving/Gold_ProductReturns/',
    FORMAT = 'PARQUET'
) AS rows;

-- Business KPI examples:
-- SELECT OrderMonth, SUM(UnitsSold) AS UnitsSold,
--        SUM(TotalOrders) AS TotalOrders,
--        SUM(OrderLineValue) AS RevenueProxy
-- FROM ServingLayer.MonthlySalesPerformance
-- GROUP BY OrderMonth
-- ORDER BY OrderMonth;
