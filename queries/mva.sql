-- IT WORKS, BUT IT IS REDICULOUSLY SLOW
  UPDATE query_data q
	SET (q.security, q.time, q.MVA_10_DAY, q.MVA_25_DAY) = 
		(SELECT q2.security, q2.time, other.mv10, other.mv25
			FROM query_data q2 LEFT OUTER JOIN 
				(SELECT q1.security, q1.time as time, AVG(q1.adj_close) 
					OVER(ORDER BY q1.time ROWS BETWEEN 9 PRECEDING 
					AND CURRENT ROW) AS mv10, AVG(q1.adj_close) 
					OVER(ORDER BY q1.time ROWS BETWEEN 24 PRECEDING 
					AND CURRENT ROW) AS mv25 FROM query_data q1
					WHERE q1.security = 'AAPL') other ON (other.time = q2.time)
			WHERE q2.security = 'AAPL' AND q.security = q2.security AND
			q.time = q2.time)
			WHERE EXISTS (SELECT 1 from query_data
				where time = q.time AND q.security = 'AAPL'
			AND security = q.security);

-- working query for mva
--SELECT q1.security, q1.time , q1.adj_close, q1.MVA_10_day, q1.MVA_25_DAY, AVG(q1.adj_close) 
--			OVER(ORDER BY q1.security ROWS BETWEEN 24 PRECEDING 
--					AND CURRENT ROW) AS mv25				
--			FROM query_data q1 
--			WHERE q1.security = 'AAPL'
--			ORDER BY q1.time;
