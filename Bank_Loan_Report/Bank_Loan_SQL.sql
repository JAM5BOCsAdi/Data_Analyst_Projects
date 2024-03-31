USE Bank_Loan_DB
-- GO;
-- ************************************* DASHBOARD 1: SUMMARY *************************************
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

-- 4.1:
SELECT 
	ROUND(AVG(int_rate), 4) * 100 AS avg_int_rate
FROM 
	Bank_Loan_DB..bank_loan_data;

-- 4.2:
SELECT 
	ROUND(AVG(int_rate), 4) * 100 AS mtd_avg_int_rate
FROM 
	Bank_Loan_DB..bank_loan_data
WHERE
	MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021;

-- 4.3:
SELECT 
	ROUND(AVG(int_rate), 4) * 100 AS pmtd_avg_int_rate
FROM 
	Bank_Loan_DB..bank_loan_data
WHERE
	MONTH(issue_date) = 11 AND YEAR(issue_date) = 2021;

-- 5:
SELECT 
	ROUND(AVG(dti), 4) * 100 AS avg_dti
FROM
	Bank_Loan_DB..bank_loan_data;

-- 5.1:
SELECT 
	ROUND(AVG(dti), 4) * 100 AS mtd_avg_dti
FROM
	Bank_Loan_DB..bank_loan_data
WHERE 
	MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021;

-- 5.2:
SELECT 
	ROUND(AVG(dti), 4) * 100 AS pmtd_avg_dti
FROM
	Bank_Loan_DB..bank_loan_data
WHERE 
	MONTH(issue_date) = 11 AND YEAR(issue_date) = 2021;

--	**************************************************************
--	Good Loan vs Bad Loan KPIs:
--	**************************************************************

-- Good Loan:

-- 1.: Good Loan Applications Percentage
SELECT 
	loan_status
FROM
	Bank_Loan_DB..bank_loan_data;

SELECT
	(
		COUNT
		(
			CASE 
				WHEN loan_status = 'Fully Paid' OR loan_status = 'Current' 
					THEN id 
			END
		) * 100
	)
	/
	COUNT(id) AS good_loan_percentage
FROM
	Bank_Loan_DB..bank_loan_data;

-- 2.: Good Loan Applications
SELECT 
	COUNT(id) AS good_loan_app
FROM 
	Bank_Loan_DB..bank_loan_data
WHERE
	loan_status = 'Fully Paid' OR loan_status = 'Current';

-- 3.: Good Loan Funded Amount
SELECT 
	SUM(loan_amount) AS good_loan_funded_amount
FROM 
	Bank_Loan_DB..bank_loan_data
WHERE
	loan_status = 'Fully Paid' OR loan_status = 'Current';

-- 4.: Good Loan Received Amount
SELECT 
	SUM(total_payment) AS good_loan_received_amount
FROM 
	Bank_Loan_DB..bank_loan_data
WHERE
	loan_status = 'Fully Paid' OR loan_status = 'Current';


-- Bad Loan:

-- 1.: Bad Loan Applications Percentage
SELECT
	(
		COUNT
		(
			CASE 
				WHEN loan_status = 'Charged Off' 
					THEN id 
			END
		) * 100.0
	)
	/
	COUNT(id) AS bad_loan_percentage
FROM
	Bank_Loan_DB..bank_loan_data;

-- 2.: Bad Loan Applications
SELECT
	COUNT(id) AS bad_loan_app
FROM
	Bank_Loan_DB..bank_loan_data
WHERE
	loan_status = 'Charged Off';

-- 3.: Bad Loan Funded Amount
SELECT
	SUM(loan_amount) AS bad_loan_funded_amount
FROM
	Bank_Loan_DB..bank_loan_data
WHERE
	loan_status = 'Charged Off';

-- 4.: Bad Loan Received Amount
SELECT
	SUM(total_payment) AS bad_loan_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
WHERE
	loan_status = 'Charged Off';

--	**************************************************************
--	Loan Status Grid View:
--	**************************************************************

-- 1.:
SELECT
	loan_status AS total_loan_applications,
	COUNT(id) AS loan_count,
	SUM(total_payment) AS total_amount_received,
	SUM(loan_amount) AS total_funded_amount,
	AVG(int_rate * 100) AS interest_rate,
	AVG(dti * 100) AS dti
FROM
	Bank_Loan_DB..bank_loan_data
GROUP BY
	loan_status;

-- 2.:
SELECT
	loan_status,
	SUM(total_payment) AS mtd_total_amount_received,
	SUM(loan_amount) AS mtd_total_funded_amount
FROM
	Bank_Loan_DB..bank_loan_data
WHERE
	MONTH(issue_date) = 12
GROUP BY
	loan_status;


-- ************************************* DASHBOARD 2: OVERVIEW *************************************
-- CHARTS:

SELECT
	*
FROM
	Bank_Loan_DB..bank_loan_data;

-- 1.: Monthly Trends by Issue Date (Line Chart)
SELECT
	MONTH(issue_date) AS month_number,
	DATENAME(MONTH, issue_date) AS month_name,
	COUNT(id) AS total_loan_applications,
	SUM(loan_amount) AS total_funded_amount,
	SUM(total_payment) AS total_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
GROUP BY
	MONTH(issue_date), DATENAME(MONTH, issue_date)
ORDER BY
	month_number;

-- An other way of doing number 1.:
-- You need to Execute the whole thing from 'WITH' to 'ORDER BY month_name DESC;'
--WITH MonthlyLoanData AS (
--    SELECT 
--        MONTH(issue_date) AS month_number,
--        DATENAME(MONTH, issue_date) AS month_name,
--        id,
--        loan_amount,
--        total_payment
--    FROM 
--        Bank_Loan_DB..bank_loan_data
--)

--SELECT 
--    month_number,
--    month_name,
--    COUNT(id) AS total_loan_applications,
--    SUM(loan_amount) AS total_funded_amount,
--    SUM(total_payment) AS total_received_amount
--FROM 
--    MonthlyLoanData
--GROUP BY 
--    month_number, month_name
--ORDER BY 
--    month_number;

-- 2.: Regional Analysis by State (Filled Map)
SELECT
	address_state,
	DATENAME(MONTH, issue_date) AS month_name,
	COUNT(id) AS total_loan_applications,
	SUM(loan_amount) AS total_funded_amount,
	SUM(total_payment) AS total_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
GROUP BY
	address_state
ORDER BY
	address_state;

SELECT
	address_state,
	COUNT(id) AS total_loan_applications,
	SUM(loan_amount) AS total_funded_amount,
	SUM(total_payment) AS total_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
GROUP BY
	address_state
ORDER BY
	SUM(loan_amount) DESC;

SELECT
	address_state,
	COUNT(id) AS total_loan_applications,
	SUM(loan_amount) AS total_funded_amount,
	SUM(total_payment) AS total_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
GROUP BY
	address_state
ORDER BY
	COUNT(id) DESC;

-- 3.: Loan Term Analysis (Donut Chart)
SELECT
	term,
	COUNT(id) AS total_loan_applications,
	SUM(loan_amount) AS total_funded_amount,
	SUM(total_payment) AS total_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
GROUP BY
	term
ORDER BY
	term;

-- 4.: Employee Length Analysis (Bar Chart)
SELECT
	emp_length,
	COUNT(id) AS total_loan_applications,
	SUM(loan_amount) AS total_funded_amount,
	SUM(total_payment) AS total_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
GROUP BY
	emp_length
ORDER BY
	emp_length;

SELECT
	emp_length,
	COUNT(id) AS total_loan_applications,
	SUM(loan_amount) AS total_funded_amount,
	SUM(total_payment) AS total_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
GROUP BY
	emp_length
ORDER BY
	COUNT(id) DESC;

-- 5.: Loan Purpose Breakdown (Bar Chart)
SELECT
	purpose,
	COUNT(id) AS total_loan_applications,
	SUM(loan_amount) AS total_funded_amount,
	SUM(total_payment) AS total_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
GROUP BY
	purpose
ORDER BY
	COUNT(id) DESC;

-- 6.: Home Ownership Analysis (Tree Map)
SELECT
	home_ownership,
	COUNT(id) AS total_loan_applications,
	SUM(loan_amount) AS total_funded_amount,
	SUM(total_payment) AS total_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
GROUP BY
	home_ownership
ORDER BY
	COUNT(id) DESC;

-- --------------------------------------------------------
SELECT
	home_ownership,
	COUNT(id) AS total_loan_applications,
	SUM(loan_amount) AS total_funded_amount,
	SUM(total_payment) AS total_received_amount
FROM
	Bank_Loan_DB..bank_loan_data
WHERE
	grade = 'A' AND address_state = 'CA'
GROUP BY
	home_ownership
ORDER BY
	COUNT(id) DESC;
