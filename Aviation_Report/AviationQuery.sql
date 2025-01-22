USE AviationDB;
GO

SELECT *
FROM AviationDB.dbo.Aviation_Data;
GO

IF OBJECT_ID('AviationView', 'V') IS NOT NULL
	BEGIN
		PRINT 'The AviationView already exists.';
	END
ELSE
	BEGIN
		PRINT 'Creating the AviationView...';
		EXEC('
			CREATE VIEW AviationView AS
			SELECT *
			FROM AviationDB.dbo.Aviation_Data;
		');
		PRINT 'The AviationView has been created successfully.';
	END;
GO

-- Checks if file exists, if not (0), prints an error. If yes, runs the file.
CREATE PROCEDURE AviationDailyStoredProcedure AS
    BEGIN
        DECLARE @Command VARCHAR(8000);
        DECLARE @FileExists INT;

		-- Enable advanced options
		EXEC sp_configure 'show advanced options', 1;
		RECONFIGURE;

		-- Enable xp_cmdshell
		EXEC sp_configure 'xp_cmdshell', 1;
		RECONFIGURE;

		-- Enable external script execution
		EXEC sp_configure 'external scripts enabled', 1;
		RECONFIGURE;


        -- Check if the Python script exists using sys.dm_os_file_exists
        SELECT @FileExists = COUNT(*)
        FROM sys.dm_os_file_exists('C:\Users\orada\Documents\Data_Analyst\Data_Analyst_Projects\Aviation_Report\Aviation_Data.py');

        PRINT 'FileExists number: ' + CAST(@FileExists AS NVARCHAR(10));

        -- If the file does not exist, print an error and exit
        IF @FileExists = 0
            BEGIN
                PRINT 'Error: The Python script does not exist.';
            END
        ELSE
            BEGIN
                -- Set the command to run the Python script
                SET @Command = 'C:\Users\orada\Documents\Data_Analyst\Data_Analyst_Projects\Aviation_Report\Aviation_Data.py';

                -- Run the command using xp_cmdshell
                EXEC xp_cmdshell @Command;

                PRINT 'Python script executed successfully.';
            END;
		
		-- Disable advanced options
		EXEC sp_configure 'show advanced options', 0;
		RECONFIGURE;

		-- Disable xp_cmdshell
		EXEC sp_configure 'xp_cmdshell', 0;
		RECONFIGURE;

		-- Disable external script execution
		EXEC sp_configure 'external scripts enabled', 1;
		RECONFIGURE;
    END;
GO

-- EXEC AviationDB.dbo.AviationDailyStoredProcedure






