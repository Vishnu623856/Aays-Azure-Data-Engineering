-- AdventureWorks Data Warehouse Structure
-- Star-schema style analytical model

-- Fact table
CREATE TABLE fact_sales (
    OrderNumber VARCHAR(20),
    OrderDate DATE,
    ProductKey INT,
    CustomerKey INT,
    TerritoryKey INT,
    OrderLineItem INT,
    OrderQuantity INT,
    LineQuantity INT
);

-- Customer dimension
CREATE TABLE dim_customer (
    CustomerKey INT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    FullName VARCHAR(200),
    Gender VARCHAR(20),
    AnnualIncome DECIMAL(18,2)
);

-- Product dimension
CREATE TABLE dim_product (
    ProductKey INT,
    ProductName VARCHAR(200),
    ProductSKU VARCHAR(100),
    ProductSubcategoryKey INT
);

-- Territory dimension
CREATE TABLE dim_territory (
    SalesTerritoryKey INT,
    Region VARCHAR(100),
    Country VARCHAR(100),
    Continent VARCHAR(100)
);

-- Date dimension
CREATE TABLE dim_date (
    DateValue DATE,
    Year INT,
    Month INT,
    MonthName VARCHAR(20),
    Quarter INT
);