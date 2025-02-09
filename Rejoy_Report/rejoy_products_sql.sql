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
		'Mobiles' AS ProductType, 
		CAST([Time] AS VARCHAR(20)) AS [Time],  -- Date + hour format (e.g., 2025-02-09_02)
		CAST(Title AS NVARCHAR(255)) AS Title,  -- Title as string
		CAST(NULL AS VARCHAR(3)) AS GPS,        -- GPS not applicable for Mobiles
		CAST(NULL AS VARCHAR(3)) AS Cellular,   -- Cellular not applicable for Mobiles
		CAST(Color AS NVARCHAR(50)) AS Color,   -- Color as string
		CAST(NULL AS INT) AS Size,              -- Size not applicable for Mobiles
		CAST([Status] AS NVARCHAR(50)) AS [Status],  -- Status as string
		CAST(Warranty AS INT) AS Warranty,      -- Warranty as number
		CAST(Price AS INT) AS Price,            -- Price as number
		CAST(Link AS NVARCHAR(500)) AS Link     -- Link as string
	FROM 
		Mobiles

	UNION ALL

	SELECT 
		'Tablets' AS ProductType, 
		CAST([Time] AS VARCHAR(20)) AS [Time],  -- Date + hour format
		CAST(Title AS NVARCHAR(255)) AS Title,  -- Title as string
		CAST(NULL AS VARCHAR(3)) AS GPS,        -- GPS not applicable for Tablets
		CAST(NULL AS VARCHAR(3)) AS Cellular,   -- Cellular not applicable for Tablets
		CAST(Color AS NVARCHAR(50)) AS Color,   -- Color as string
		CAST(NULL AS INT) AS Size,              -- Size not applicable for Tablets
		CAST([Status] AS NVARCHAR(50)) AS [Status],  -- Status as string
		CAST(Warranty AS INT) AS Warranty,      -- Warranty as number
		CAST(Price AS INT) AS Price,            -- Price as number
		CAST(Link AS NVARCHAR(500)) AS Link     -- Link as string
	FROM 
		Tablets

	UNION ALL

	SELECT 
		'Laptops' AS ProductType, 
		CAST([Time] AS VARCHAR(20)) AS [Time],  -- Date + hour format
		CAST(Title AS NVARCHAR(255)) AS Title,  -- Title as string
		CAST(NULL AS VARCHAR(3)) AS GPS,        -- GPS not applicable for Laptops
		CAST(NULL AS VARCHAR(3)) AS Cellular,   -- Cellular not applicable for Laptops
		CAST(Color AS NVARCHAR(50)) AS Color,   -- Color as string
		CAST(NULL AS INT) AS Size,              -- Size not applicable for Laptops
		CAST([Status] AS NVARCHAR(50)) AS [Status],  -- Status as string
		CAST(Warranty AS INT) AS Warranty,      -- Warranty as number
		CAST(Price AS INT) AS Price,            -- Price as number
		CAST(Link AS NVARCHAR(500)) AS Link     -- Link as string
	FROM 
		Laptops

	UNION ALL

	SELECT 
		'Smartwatches' AS ProductType, 
		CAST([Time] AS VARCHAR(20)) AS [Time],  -- Date + hour format
		CAST(Title AS NVARCHAR(255)) AS Title,  -- Title as string
		CAST(GPS AS VARCHAR(3)) AS GPS,         -- GPS as Yes/No
		CAST(Cellular AS VARCHAR(3)) AS Cellular,  -- Cellular as Yes/No
		CAST(Color AS NVARCHAR(50)) AS Color,   -- Color as string
		CAST(Size AS INT) AS Size,              -- Size as number
		CAST([Status] AS NVARCHAR(50)) AS [Status],  -- Status as string
		CAST(Warranty AS INT) AS Warranty,      -- Warranty as number
		CAST(Price AS INT) AS Price,            -- Price as number
		CAST(Link AS NVARCHAR(500)) AS Link     -- Link as string
	FROM 
		Smartwatches
;
GO

SELECT * FROM vw_AllProducts;
