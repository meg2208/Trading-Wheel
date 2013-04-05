-- CROSS OVER
Select * 
  FROM ( 
		SELECT q.time, SUM(q.MVA_10_day) OVER(ORDER BY q.time ROWS BETWEEN 1 PRECEDING 
				AND CURRENT ROW) - q.MVA_10_day AS yestmva1, q.mva_10_day AS mva1,
			SUM(q.MVA_25_day) OVER(ORDER BY q.time ROWS BETWEEN 1 PRECEDING 
				AND CURRENT ROW) - q.mva_25_day AS yestmva2, q.mva_25_day AS mva2
		FROM query_data q
		WHERE q.security = 'AAPL')
	WHERE mva1 > mva2 AND yestmva1 < yestmva2; 
