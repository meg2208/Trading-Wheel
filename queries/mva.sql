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