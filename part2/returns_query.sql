--annual returns
SELECT 	year, 
		ROUND(((a2.portfolio_value - a1.portfolio_value) / 
				a1.portfolio_value)*100, 2) as portfolio_returns, 
		ROUND(((a2.bench_values.value - a1.bench_values.value) / 
					a1.bench_values.value)*100, 2) as bench_returns
 	FROM (
 			SELECT MIN(a.time) as start_time, MAX(a.time) as end_time,
					EXTRACT (year FROM a.time) as year
			FROM   analysis a
			WHERE a.strategy_id = 1066
			GROUP BY extract(year FROM a.time)
			ORDER BY year
 		 ) b LEFT OUTER JOIN analysis a1 ON a1.time = start_time AND a1.strategy_id = 1066
 			 LEFT OUTER JOIN analysis a2 ON a2.time = end_time AND a2.strategy_id = 1066
 	ORDER BY a1.time;