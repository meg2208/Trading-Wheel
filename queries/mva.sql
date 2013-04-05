-- quickly calculates and populates mva data
MERGE INTO query_data A 
USING (SELECT DISTINCT q.time, AVG(q.adj_close) OVER(ORDER BY q.time ROWS BETWEEN 9 PRECEDING 
			AND CURRENT ROW) AS mv10,
			AVG(q.adj_close) OVER(ORDER BY q.time ROWS BETWEEN 24 PRECEDING 
			AND CURRENT ROW) AS mv25 
		FROM query_data q
		WHERE q.security = 'AAPL') B
	ON (A.time = B.time AND A.security = 'AAPL')
	WHEN MATCHED THEN UPDATE SET A.MVA_10_day = B.mv10, A.MVA_25_DAY = B.mv25;



-- deletes row	
-- UPDATE query_data SET MVA_10_day = NULL, MVA_25_DAY = NULL where security = 'AAPL';

-- queries data
-- SELECT * from query_data where security = 'AAPL' order by time;


-- working query for mva
--SELECT q1.security, q1.time , q1.adj_close, q1.MVA_10_day, q1.MVA_25_DAY, AVG(q1.adj_close) 
--			OVER(ORDER BY q1.security ROWS BETWEEN 24 PRECEDING 
--					AND CURRENT ROW) AS mv25				
--			FROM query_data q1 
--			WHERE q1.security = 'AAPL'
--			ORDER BY q1.time;
