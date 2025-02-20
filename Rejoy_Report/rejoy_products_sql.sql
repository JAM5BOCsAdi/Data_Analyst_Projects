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
		CAST([Time] AS VARCHAR(20)) AS [Time],
		CAST(Title AS NVARCHAR(255)) AS Title,
		CAST(NULL AS VARCHAR(100)) AS CPU,        
		CAST(NULL AS VARCHAR(100)) AS RAM,        
		CAST(NULL AS VARCHAR(100)) AS Graphics,   
		CAST(Memory AS NVARCHAR(50)) AS Color,   -- Memory is now stored in Color column for Mobiles
		CAST(Color AS NVARCHAR(100)) AS Memory,  -- Color is now stored in Memory column for Mobiles
		CAST(NULL AS INT) AS Size,              
		CAST([Status] AS NVARCHAR(50)) AS [Status],  
		CAST(Warranty AS INT) AS Warranty_Years,  
		CAST(Price AS INT) AS Price,            
		CAST(Link AS NVARCHAR(500)) AS Link     
	FROM 
		Mobiles

	UNION ALL

	SELECT 
		'Tablets' AS Product_Type, 
		CAST([Time] AS VARCHAR(20)) AS [Time],
		CAST(Title AS NVARCHAR(255)) AS Title,
		CAST(NULL AS VARCHAR(100)) AS CPU,        
		CAST(NULL AS VARCHAR(100)) AS RAM,        
		CAST(NULL AS VARCHAR(100)) AS Graphics,   
		CAST(Memory AS NVARCHAR(50)) AS Color,   -- Memory is now stored in Color column for Tablets
		CAST(Color AS NVARCHAR(100)) AS Memory,  -- Color is now stored in Memory column for Tablets
		CAST(NULL AS INT) AS Size,              
		CAST([Status] AS NVARCHAR(50)) AS [Status],  
		CAST(Warranty AS INT) AS Warranty_Years,  
		CAST(Price AS INT) AS Price,            
		CAST(Link AS NVARCHAR(500)) AS Link     
	FROM 
		Tablets

	UNION ALL

	SELECT 
		'Laptops' AS Product_Type, 
		CAST([Time] AS VARCHAR(20)) AS [Time],
		CAST(Title AS NVARCHAR(255)) AS Title,
		CAST(CPU AS VARCHAR(100)) AS CPU,         
		CAST(RAM AS VARCHAR(100)) AS RAM,         
		CAST(Graphics AS VARCHAR(100)) AS Graphics,  
		CAST(Color AS NVARCHAR(50)) AS Color,   
		CAST(Memory AS VARCHAR(100)) AS Memory,  -- Memory is kept for Laptops
		CAST(NULL AS INT) AS Size,              
		CAST([Status] AS NVARCHAR(50)) AS [Status],  
		CAST(Warranty AS INT) AS Warranty_Years,  
		CAST(Price AS INT) AS Price,            
		CAST(Link AS NVARCHAR(500)) AS Link     
	FROM 
		Laptops

	UNION ALL

	SELECT 
		'Smartwatches' AS Product_Type, 
		CAST([Time] AS VARCHAR(20)) AS [Time],
		CAST(Title AS NVARCHAR(255)) AS Title,
		CAST(NULL AS VARCHAR(100)) AS CPU,        
		CAST(NULL AS VARCHAR(100)) AS RAM,        
		CAST(NULL AS VARCHAR(100)) AS Graphics,   
		CAST(Color AS NVARCHAR(50)) AS Color,   
		CAST(NULL AS VARCHAR(100)) AS Memory,  -- Memory is not applicable for Smartwatches
		CAST(Size AS INT) AS Size,              
		CAST([Status] AS NVARCHAR(50)) AS [Status],  
		CAST(Warranty AS INT) AS Warranty_Years,  
		CAST(Price AS INT) AS Price,            
		CAST(Link AS NVARCHAR(500)) AS Link     
	FROM 
		Smartwatches
;
GO

SELECT *
FROM vw_AllProducts;


SELECT *
FROM Laptops

SELECT *
FROM Mobiles

SELECT *
FROM Smartwatches

SELECT *
FROM Tablets


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


