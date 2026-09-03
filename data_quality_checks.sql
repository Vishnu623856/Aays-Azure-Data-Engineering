-- Data quality checks for the Synapse serving layer.
-- These queries can be used as pipeline validation activities.

-- 1. Null order identifiers
SELECT COUNT(*) AS NullOrderNumbers
FROM ServingLayer.Sales
WHERE OrderNumber IS NULL;

-- 2. Invalid quantities
SELECT COUNT(*) AS InvalidQuantities
FROM ServingLayer.Sales
WHERE OrderQuantity <= 0;

-- 3. Duplicate order-line records
SELECT OrderNumber, ProductKey, OrderLineItem, COUNT(*) AS DuplicateCount
FROM ServingLayer.Sales
GROUP BY OrderNumber, ProductKey, OrderLineItem
HAVING COUNT(*) > 1;

-- 4. Referential integrity: sales with unknown products
SELECT COUNT(*) AS OrphanProductKeys
FROM ServingLayer.Sales s
LEFT JOIN ServingLayer.Products p
    ON s.ProductKey = p.ProductKey
WHERE p.ProductKey IS NULL;
