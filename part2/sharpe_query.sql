SELECT 	c.avg_excess / c.s_dev as Sharpe_ratio
FROM	(SELECT	STDDEV( 
					((a2.portfolio_value-a1.portfolio_value)/a1.portfolio_value)
				- ((a2.bench_values.value-a1.bench_values.value)/a1.bench_values.value)
				) as s_dev,
				AVG(
					((a2.portfolio_value-a1.portfolio_value)/a1.portfolio_value)
						- ((a2.bench_values.value-a1.bench_values.value)/a1.bench_values.value)
				) as avg_excess
	 	FROM (
	 			SELECT MIN(a.time) as start_time, MAX(a.time) as end_time,
						EXTRACT (year FROM a.time) as year
				FROM   analysis a
				WHERE a.strategy_id = 1066
				GROUP BY extract(year FROM a.time)
				ORDER BY year
	 		 ) b LEFT OUTER JOIN analysis a1 ON a1.time = b.start_time AND a1.strategy_id = 1066
	 			 LEFT OUTER JOIN analysis a2 ON a2.time = b.end_time AND a2.strategy_id = 1066
	 	ORDER BY a1.time) c;