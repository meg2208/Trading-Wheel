MERGE INTO query_data A 
USING (SELECT DISTINCT q.time, 
	AVG(q.security) OVER(ORDER BY q.time ROWS BETWEEN 25-1 PRECEDING 
			AND CURRENT ROW) AS mv25, AVG(q.security) OVER(ORDER BY q.time ROWS BETWEEN 10-1 PRECEDING 
			AND CURRENT ROW)
		FROM query_data q, raw_data_parsing rdp
		WHERE rdp.strategy_id = 1000
		q.security = {0}
		ORDER BY q.security) B
	ON (A.time = B.time AND A.security = q.security)
	WHEN MATCHED THEN UPDATE SET A.MVA_25_DAY = B.mv25, 
								A.MVA_10_DAY = B.mv10