USE Bank_Loan_DB
GO;

SELECT
	*
FROM
--	New Style:
	Bank_Loan_DB..bank_loan_data;
--	Old Style:
--	Bank_Loan_DB.dbo.bank_loan_data;
 
--	**************************************************************
--	Key Performance Indicators (KPIs) Requirements:
--	**************************************************************

-- 1:
SELECT 
	COUNT(id) AS total_loan_applications
FROM
	Bank_Loan_DB..bank_loan_data;

-- 1.1:
-- MTD: Month To Date
SELECT 
	COUNT(id)AS mtd_total_loan_applications
FROM
	Bank_Loan_DB..bank_loan_data
WHERE
	MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021;

-- THIS IS HOW YOU CAN ADD TEXT TO THE RESULTS:
--SELECT 
--	CAST(COUNT(id) AS VARCHAR(20)) + ' day(s)' AS mtd_total_loan_applications
--FROM
--	Bank_Loan_DB..bank_loan_data
--WHERE
--	MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021;

-- 1.2:
-- PMTD: Previous Month To Date
SELECT 
	COUNT(id) AS pmtd_total_loan_applications
FROM
	Bank_Loan_DB..bank_loan_data
WHERE
	MONTH(issue_date) = 11 AND YEAR(issue_date) = 2021;

-- 2:
SELECT
	SUM(loan_amount) AS total_funded_amount
FROM Bank_Loan_DB..bank_loan_data;

-- 2.1:
-- MTD: Month To Date
SELECT
	SUM(loan_amount) AS mtd_total_funded_amount
FROM 
	Bank_Loan_DB..bank_loan_data
WHERE
	MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021;

-- 2.2:
-- PMTD: Previous Month To Date
SELECT
	SUM(loan_amount) AS pmtd_total_funded_amount
FROM 
	Bank_Loan_DB..bank_loan_data
WHERE
	MONTH(issue_date) = 11 AND YEAR(issue_date) = 2021;

-- 3:
SELECT
	SUM(total_payment) AS mtd_total_amount_received
FROM
	Bank_Loan_DB..bank_loan_data
WHERE 
	MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021;

-- 3.1:
SELECT
	SUM(total_payment) AS pmtd_total_amount_received
FROM
	Bank_Loan_DB..bank_loan_data
WHERE 
	MONTH(issue_date) = 11 AND YEAR(issue_date) = 2021;

-- 4.:
SELECT 
	AVG(int_rate) * 100 AS avg_int_rate
FROM 
	Bank_Loan_DB..bank_loan_data;

