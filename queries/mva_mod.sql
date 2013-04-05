MERGE INTO query_data A 
USING (SELECT DISTINCT q.time, AVG(q.{1}) OVER(ORDER BY q.time ROWS BETWEEN {3} PRECEDING 
			AND CURRENT ROW) AS mv10
		FROM query_data q
		WHERE q.security = '{0}') B
	ON (A.time = B.time AND A.security = '{0}')
	WHEN MATCHED THEN UPDATE SET A.{2} = B.mv10