--	UPDATE (SELECT q1.security, q1.time ,q1.MVA_10_day, q1.MVA_25_DAY			
--			FROM query_data q1 
--			WHERE q1.security = 'AAPL') to_update
--	SET (to_update.time, to_update.MVA_10_day, to_update.MVA_25_DAY) = 
--		(SELECT DISTINCT q2.time, AVG(q2.adj_close) OVER(ORDER BY q2.time ROWS BETWEEN 9 PRECEDING 
--					AND CURRENT ROW) AS mv10, 
--			AVG(q2.adj_close) OVER(ORDER BY q2.time ROWS BETWEEN 24 PRECEDING 
--					AND CURRENT ROW) AS mv25 
--			FROM query_data q2
--			WHERE q2.security = 'AAPL'
--			WHERE q2.security = to_update.security AND q2.time = to_update.time
--		) where time in to_update.time;

--	UPDATE query_data SET MVA_10_day = NULL, MVA_25_DAY = NULL where security = 'AAPL';
--	MERGE INTO query_data A 
--	USING (SELECT DISTINCT q.time, AVG(q.adj_close) OVER(ORDER BY q.time ROWS BETWEEN 9 PRECEDING 
--					AND CURRENT ROW) AS mv10, 
--			AVG(q.adj_close) OVER(ORDER BY q.time ROWS BETWEEN 24 PRECEDING 
--					AND CURRENT ROW) AS mv25 
--			FROM query_data q
--			WHERE q.security = 'AAPL') B
--	ON (A.time = B.time AND A.security = 'AAPL')
--	WHEN MATCHED THEN UPDATE SET A.MVA_10_day = B.mv10, A.MVA_25_DAY = B.mv25;
--	SELECT * from query_data where security = 'AAPL' order by time;

	Select * 
		FROM ( 
			SELECT q.time, SUM(q.MVA_10_day) OVER(ORDER BY q.time ROWS BETWEEN 1 PRECEDING 
					AND CURRENT ROW) - q.MVA_10_day AS yestmva1, q.mva_10_day AS mva1,
				SUM(q.MVA_25_day) OVER(ORDER BY q.time ROWS BETWEEN 1 PRECEDING 
					AND CURRENT ROW) - q.mva_25_day AS yestmva2, q.mva_25_day AS mva2
			FROM query_data q
			WHERE q.security = 'AAPL')
			WHERE mva1 > mva2 AND yestmva1 < yestmva2;

	-- POPULATE X_OVER/X_UNDER FOR USER WHEN CROSS OVER
	

--	ON (A.time = B.time AND A.security = 'AAPL')
--	WHEN MATCHED THEN UPDATE SET A.MVA_10_day = B.mv10, A.MVA_25_DAY = B.mv25;
--	SELECT * from query_data where security = 'AAPL' order by time;

--x			WHERE q2.security = to_update.security AND q2.time = to_update.time
	--	x) where time in to_update.time;

 
--			EXISTS (SELECT 1 from query_data
--				where time = q.time AND q.security = 'AAPL'
--			AND security = q.security);