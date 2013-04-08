Select q.time, 	q.adj_close
  FROM ( 
		SELECT q.time, SUM(q.{1}) OVER(ORDER BY q.time ROWS BETWEEN 1 PRECEDING 
				AND CURRENT ROW) - q.{1} AS yestmva1, q.{1} AS mva1,
			SUM(q.{2}) OVER(ORDER BY q.time ROWS BETWEEN 1 PRECEDING 
				AND CURRENT ROW) - q.{2} AS yestmva2, q.{2} AS mva2
		FROM query_data q
		WHERE q.security = {0})
	WHERE mva1 > mva2 AND yestmva1 < yestmva2