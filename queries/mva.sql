MERGE INTO query_data A 
USING (SELECT q.security, q.time, 
	AVG(q.adj_close) OVER(ORDER BY q.time ROWS BETWEEN 25-1 PRECEDING 
			AND CURRENT ROW) AS mv25, AVG(q.adj_close) OVER(ORDER BY q.time ROWS BETWEEN 10-1 PRECEDING 
			AND CURRENT ROW) AS mv10
		FROM query_data q, raw_data_parsing rdp
		WHERE rdp.strategy_id = {0}
			AND rdp.security = q.security
			AND rdp.time = q.time
		ORDER BY q.security) B
	ON (A.time = B.time AND A.security = B.security)
	WHEN MATCHED THEN UPDATE SET A.MVA_25_DAY = B.mv25, 
								A.MVA_10_DAY = B.mv10
