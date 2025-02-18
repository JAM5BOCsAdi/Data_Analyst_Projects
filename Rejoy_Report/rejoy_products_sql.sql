USE RejoyProducts
GO

IF EXISTS (SELECT * FROM sys.views WHERE name = 'vw_AllProducts')
BEGIN
    DROP VIEW vw_AllProducts;
    PRINT 'vw_AllProducts DROPPED';
END;
GO

CREATE VIEW vw_AllProducts AS
	SELECT 
		'Mobiles' AS Product_Type, 
		CAST([Time] AS VARCHAR(20)) AS [Time],  -- Date + hour format (e.g., 2025-02-09_02)
		CAST(Title AS NVARCHAR(255)) AS Title,  -- Title as string
		CAST(NULL AS VARCHAR(3)) AS GPS,        -- GPS not applicable for Mobiles
		CAST(NULL AS VARCHAR(3)) AS Cellular,   -- Cellular not applicable for Mobiles
		CAST(Color AS NVARCHAR(50)) AS Color,   -- Color as string
		CAST(NULL AS INT) AS Size,              -- Size not applicable for Mobiles
		CAST([Status] AS NVARCHAR(50)) AS [Status],  -- Status as string
		CAST(Warranty AS INT) AS Warranty_Years, -- Extract numeric part
		CAST(Price AS INT) AS Price,            -- Price as number
		CAST(Link AS NVARCHAR(500)) AS Link     -- Link as string
	FROM 
		Mobiles

	UNION ALL

	SELECT 
		'Tablets' AS Product_Type, 
		CAST([Time] AS VARCHAR(20)) AS [Time],  -- Date + hour format
		CAST(Title AS NVARCHAR(255)) AS Title,  -- Title as string
		CAST(NULL AS VARCHAR(3)) AS GPS,        -- GPS not applicable for Tablets
		CAST(NULL AS VARCHAR(3)) AS Cellular,   -- Cellular not applicable for Tablets
		CAST(Color AS NVARCHAR(50)) AS Color,   -- Color as string
		CAST(NULL AS INT) AS Size,              -- Size not applicable for Tablets
		CAST([Status] AS NVARCHAR(50)) AS [Status],  -- Status as string
		CAST(Warranty AS INT) AS Warranty_Years,  -- Extract numeric part
		CAST(Price AS INT) AS Price,            -- Price as number
		CAST(Link AS NVARCHAR(500)) AS Link     -- Link as string
	FROM 
		Tablets

	UNION ALL

	SELECT 
		'Laptops' AS Product_Type, 
		CAST([Time] AS VARCHAR(20)) AS [Time],  -- Date + hour format
		CAST(Title AS NVARCHAR(255)) AS Title,  -- Title as string
		CAST(NULL AS VARCHAR(3)) AS GPS,        -- GPS not applicable for Laptops
		CAST(NULL AS VARCHAR(3)) AS Cellular,   -- Cellular not applicable for Laptops
		CAST(Color AS NVARCHAR(50)) AS Color,   -- Color as string
		CAST(NULL AS INT) AS Size,              -- Size not applicable for Laptops
		CAST([Status] AS NVARCHAR(50)) AS [Status],  -- Status as string
		CAST(Warranty AS INT) AS Warranty_Years,  -- Extract numeric part
		CAST(Price AS INT) AS Price,            -- Price as number
		CAST(Link AS NVARCHAR(500)) AS Link     -- Link as string
	FROM 
		Laptops

	UNION ALL

	SELECT 
		'Smartwatches' AS Product_Type, 
		CAST([Time] AS VARCHAR(20)) AS [Time],  -- Date + hour format
		CAST(Title AS NVARCHAR(255)) AS Title,  -- Title as string
		CAST(GPS AS VARCHAR(3)) AS GPS,         -- GPS as Yes/No
		CAST(Cellular AS VARCHAR(3)) AS Cellular,  -- Cellular as Yes/No
		CAST(Color AS NVARCHAR(50)) AS Color,   -- Color as string
		CAST(Size AS INT) AS Size,              -- Size as number
		CAST([Status] AS NVARCHAR(50)) AS [Status],  -- Status as string
		CAST(Warranty AS INT) AS Warranty_Years,  -- Extract numeric part
		CAST(Price AS INT) AS Price,            -- Price as number
		CAST(Link AS NVARCHAR(500)) AS Link     -- Link as string
	FROM 
		Smartwatches
;
GO

SELECT * FROM vw_AllProducts
ORDER BY [Time] DESC;




SELECT SUM(Price) AS Total_Price
FROM vw_AllProducts;

-- TOP 1 Product / Category  by Price
WITH RankedProducts AS (
    SELECT 
        Product_Type, 
        Title, 
        Price, 
        ROW_NUMBER() OVER (PARTITION BY Product_Type ORDER BY Price DESC) AS Rank
    FROM vw_AllProducts
)
SELECT Product_Type, Title, Price
FROM RankedProducts
WHERE Rank = 1;





EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

EXEC xp_cmdshell 'python "C:/Users/orada/Documents/Data_Analyst/Data_Analyst_Projects/Rejoy_Report/rejoy_web_scrape.py"'

EXEC sp_configure 'xp_cmdshell', 0;
RECONFIGURE;
EXEC sp_configure 'show advanced options', 0;
RECONFIGURE;

EXEC xp_cmdshell 'whoami'


SELECT Warranty
FROM Laptops

SELECT Warranty
FROM Mobiles

SELECT Warranty
FROM Smartwatches

SELECT Warranty
FROM Tablets