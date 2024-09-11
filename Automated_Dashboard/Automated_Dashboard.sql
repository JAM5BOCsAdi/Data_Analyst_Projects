USE Automated_Database
;
GO

--IF OBJECT_ID('gdp_raw_data') IS NOT NULL DROP TABLE gdp_raw_data;
--GO

--CREATE TABLE gdp_raw_data(
--	DEMO_IND NVARCHAR(200),
--	INDICATOR NVARCHAR(200),
--	LOCATION NVARCHAR(200),
--	COUNTRY NVARCHAR(200),
--	TIME NVARCHAR(200),
--	VALUE FLOAT --> NVARCHAR(200) Works, because there are numbers, that are 1.234E +11 format.
--);

--SELECT *
--FROM Automated_Database.dbo.gdp_raw_data
--;

---- Import Data:
--BULK INSERT Automated_Database.dbo.gdp_raw_data
--FROM 'C:\Users\orada\Documents\Data_Analyst\Data_Analyst_Projects\Automated_Dashboard\gdp_raw_data.csv'
--WITH (FORMAT='CSV')

--DROP VIEW GDP_Excel_Input


-- CREATE VIEW ERROR "CREATE VIEW must be the only statement in the batch"
-- Need to put GO around
-- https://stackoverflow.com/questions/27272194/create-view-must-be-the-only-statement-in-the-batch

--OBJECT_ID Function and Its Parameters
--OBJECT_ID('object_name', 'P'): Checks if a stored procedure exists. The 'P' stands for "Procedure".
--OBJECT_ID('object_name', 'U'): Checks if a user-defined table exists. The 'U' stands for "User table".
--OBJECT_ID('object_name', 'V'): Checks if a view exists. The 'V' stands for "View".
--OBJECT_ID('object_name', 'FN'): Checks if a scalar function exists. The 'FN' stands for "Function".
--OBJECT_ID('object_name', 'TF'): Checks if a table-valued function exists. The 'TF' stands for "Table-valued Function".
--OBJECT_ID('object_name', 'P'): Checks if a stored procedure exists. The 'P' stands for "Procedure".

IF OBJECT_ID('GDP_Excel_Input', 'V') IS NOT NULL
    DROP VIEW GDP_Excel_Input
;
GO

CREATE VIEW GDP_Excel_Input AS
	SELECT a.*, b.GDP_Per_Capita
	FROM
		(SELECT COUNTRY, TIME AS Year_No, VALUE AS GDP_Value
		FROM Automated_Database.dbo.gdp_raw_data
		WHERE INDICATOR = 'GDP (current US$)') a

	LEFT JOIN
		(SELECT COUNTRY, TIME AS Year_No, VALUE AS GDP_Per_Capita
		FROM Automated_Database.dbo.gdp_raw_data
		WHERE INDICATOR = 'GDP per capita (current US$)' ) b
		ON a.COUNTRY = b.COUNTRY AND a.Year_No = b.Year_No
;
GO


SELECT *
FROM Automated_Database.dbo.GDP_Excel_Input
;
GO

-- Drop the existing stored procedure if it exists
IF OBJECT_ID('GDP_Excel_Input_Monthly', 'P') IS NOT NULL
    DROP PROCEDURE GDP_Excel_Input_Monthly
;
GO

-- Create the new stored procedure
CREATE PROCEDURE GDP_Excel_Input_Monthly AS
	BEGIN
		-- Drop the existing table if it exists
		IF OBJECT_ID('Automated_Database.dbo.gdp_raw_data', 'U') IS NOT NULL
			DROP TABLE Automated_Database.dbo.gdp_raw_data;

		-- Create the table
		CREATE TABLE Automated_Database.dbo.gdp_raw_data(
			DEMO_IND NVARCHAR(200),
			INDICATOR NVARCHAR(200),
			LOCATION NVARCHAR(200),
			COUNTRY NVARCHAR(200),
			TIME NVARCHAR(200),
			VALUE NVARCHAR(200) -- NVARCHAR(200) Works, because there are numbers in 1.234E+11 format.
		);

		-- Bulk insert data into the table, skipping the header row
		BULK INSERT Automated_Database.dbo.gdp_raw_data
		FROM 'C:\Users\{user}\Documents\Data_Analyst\Data_Analyst_Projects\Automated_Dashboard\gdp_raw_data.csv'
		WITH (
			FORMAT='CSV',
			FIRSTROW=2 -- Skip the first row (header row)
		);

		-- Select all data from the table to verify the insertion
		SELECT *
		FROM Automated_Database.dbo.gdp_raw_data;
	END
;
GO

-- Execute the stored procedure to test it
EXEC GDP_Excel_Input_Monthly
;
GO

