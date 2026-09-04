-- AdventureWorks Analytics Queries
-- SQL serving/analytics layer

-- 1. Total records by year
SELECT
    OrderYear,
    COUNT(*) AS TotalSalesRecords,
    SUM(OrderQuantity) AS TotalQuantity
FROM silver_sales
GROUP BY OrderYear
ORDER BY OrderYear;


-- 2. Monthly sales performance
SELECT
    OrderYear,
    OrderMonth,
    COUNT(DISTINCT OrderNumber) AS TotalOrders,
    SUM(OrderQuantity) AS TotalQuantity
FROM silver_sales
GROUP BY
    OrderYear,
    OrderMonth
ORDER BY
    OrderYear,
    OrderMonth;


-- 3. Top 10 products by quantity
SELECT
    ProductKey,
    SUM(OrderQuantity) AS TotalQuantity,
    COUNT(DISTINCT OrderNumber) AS TotalOrders
FROM silver_sales
GROUP BY ProductKey
ORDER BY TotalQuantity DESC
LIMIT 10;


-- 4. Top customers by number of orders
SELECT
    CustomerKey,
    COUNT(DISTINCT OrderNumber) AS TotalOrders,
    SUM(OrderQuantity) AS TotalQuantity
FROM silver_sales
GROUP BY CustomerKey
ORDER BY TotalOrders DESC
LIMIT 10;


-- 5. Sales by territory
SELECT
    TerritoryKey,
    COUNT(DISTINCT OrderNumber) AS TotalOrders,
    SUM(OrderQuantity) AS TotalQuantity
FROM silver_sales
GROUP BY TerritoryKey
ORDER BY TotalQuantity DESC;


-- 6. Overall sales summary
SELECT
    COUNT(DISTINCT OrderNumber) AS TotalOrders,
    COUNT(DISTINCT CustomerKey) AS TotalCustomers,
    COUNT(DISTINCT ProductKey) AS TotalProducts,
    SUM(OrderQuantity) AS TotalQuantity
FROM silver_sales;