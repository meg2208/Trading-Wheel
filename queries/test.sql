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

INSERT INTO RAW_DATA_PARSING (strategy_id, security, time) 
	SELECT {0}, q.security, q.time
	FROM indicator_reference ir, criteria c,
		criteria c1, query_data q
	WHERE 
		q.time >= ir.start_time AND
		q.time <= ir.end_time AND
		ir.buy_sell = 'S' AND
		q.security = ir.action_security AND
		ir.L_Indicator_ID = c1.indicator_id AND
		ir.R_Indicator_id = c.indicator_id AND
		c.strategy_id = c1.strategy_id AND
		c1.strategy_id = {0} AND
		NOT EXISTS
		(SELECT * 
			FROM raw_data_parsing r1
			WHERE r1.strategy_id = {0} 
			AND r1.security = q.security
				AND r1.time = q.time);



	-- POPULATE X_OVER/X_UNDER FOR USER WHEN CROSS OVER
	

--	ON (A.time = B.time AND A.security = 'AAPL')
--	WHEN MATCHED THEN UPDATE SET A.MVA_10_day = B.mv10, A.MVA_25_DAY = B.mv25;
--	SELECT * from query_data where security = 'AAPL' order by time;

--x			WHERE q2.security = to_update.security AND q2.time = to_update.time
	--	x) where time in to_update.time;

 
--			EXISTS (SELECT 1 from query_data
--				where time = q.time AND q.security = 'AAPL'
--			AND security = q.security);