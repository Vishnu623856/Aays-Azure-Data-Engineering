------------------------------------------------
----GETTING INSIGHTS FROM THE AZURE DATABASE
------------------------------------------------

SELECT * FROM ServingLayer.Customers_det;

---TOTAL MALE CUSTOMERS
SELECT 
    COUNT(*)
AS
    'TOTAL MALE CUSTOMERS'
FROM 
    ServingLayer.Customers_det 
WHERE 
    Gender = 'M';

---TOTAL FEMALE CUSTOMERS
SELECT 
    COUNT(*)
AS
    'TOTAL FEMALE CUSTOMERS'
FROM 
    ServingLayer.Customers_det 
WHERE 
    Gender = 'F';

---COUNT OF MARRIED CUSTOMERS
SELECT
    COUNT(*)
AS
    'MARRIED CUSTOMERS'
FROM 
    ServingLayer.Customers_det 
WHERE 
    MaritalStatus = 'M';
    
---COUNT OF UNMARRIED CUSTOMERS
SELECT
    COUNT(*)
AS
    'UNMARRIED CUSTOMERS'
FROM 
    ServingLayer.Customers_det 
WHERE 
    MaritalStatus = 'S';

---CUSTOMERS WHOSE ANNUAL INCOME IS MORE THAN $30,000
SELECT *
FROM 
    ServingLayer.Customers_det
WHERE
    AnnualIncome > 30000;

---COUNT OF CUSTOMERS WHOSE OCCUPATION IS 'PROFESSIONAL' OR 'MANAGEMENT'
SELECT
    COUNT(*)
FROM
    ServingLayer.Customers_det
WHERE 
    Occupation = 'Professional' or Occupation = 'Management';

---HIGH COST PRODUCT
SELECT * FROM ServingLayer.Products;

SELECT TOP 1 
    ProductName, ProductDescription, ProductCost
FROM 
    ServingLayer.Products
ORDER BY 
    ProductCost DESC;

---TOP 5 HIGH SOLD PRODUCTS
SELECT * FROM ServingLayer.Products;

SELECT TOP 5
    S.ProductKey, 
    SUM(S.OrderQuantity) AS 'TOTAL_ORDER_QUANTITY',
    P.ProductName, 
    P.ProductDescription
FROM 
    ServingLayer.Sales S 
INNER JOIN 
    ServingLayer.Products P
ON 
    S.ProductKey = P.ProductKey
GROUP BY 
    S.ProductKey, P.ProductName, P.ProductDescription
ORDER BY
    SUM(S.OrderQuantity) DESC; 


--HIGH RETURNED PRODUCT
SELECT * FROM ServingLayer.RETURNS;


SELECT TOP 3
    R.ProductKey, 
    SUM(R.ReturnQuantity) AS 'TOTAL_RETURN_QUANTITY', 
    P.ProductName,
    P.ProductDescription
FROM 
    ServingLayer.Returns R 
INNER JOIN 
    ServingLayer.Products P
ON 
    R.ProductKey = P.ProductKey
GROUP BY 
    R.ProductKey, P.ProductName, P.ProductDescription
ORDER BY 
    SUM(ReturnQuantity)
    DESC;

select * from ServingLayer.Territories;

--- HIGH ORDER REGION, COUNTRY, CONTINENT
SELECT TOP 3
    T.SalesTerritoryKey,
    COUNT(S.OrderNumber) AS 'TOTAL_ORDERS',
    T.Region,
    T.Country,
    T.Continent
FROM 
    ServingLayer.Territories T 
INNER JOIN 
    ServingLayer.Sales S
ON 
    T.SalesTerritoryKey = S.TerritoryKey
GROUP BY 
    T.SalesTerritoryKey,
    T.Region,
    T.Country,
    T.Continent
ORDER BY 
    COUNT(S.OrderNumber) 
    DESC;

select * from ServingLayer.Sales;
--- TOP 5 HIGH ORDER CUSTOMERS
SELECT TOP 5
    C.FullName,
    COUNT(S.OrderNumber) AS 'TOTAL_ORDER'
FROM 
    ServingLayer.Customers_det C
INNER JOIN 
    ServingLayer.Sales S     
ON 
    C.CustomerKey = S.CustomerKey
GROUP BY 
    C.FullName
ORDER BY 
    COUNT(S.OrderNumber) 
    DESC;