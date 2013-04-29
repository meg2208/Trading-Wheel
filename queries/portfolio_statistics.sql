SELECT ROUND(((ag2.portfolio_value - ag1.portfolio_value) / ag1.portfolio_value)*100, 2) as returns,
		CAST(year as CHAR(4)) as year
 	FROM (
 			SELECT MIN(ag.time) as start_time, MAX(ag.time) as end_time,
					EXTRACT (year FROM ag.time) as year
			FROM   aggregate_portfolio ag, day_to_day dtd
			WHERE ag.portfolio_id = dtd.portfolio_id
				AND dtd.strategy_id = {0}
			GROUP BY extract(year FROM ag.time)
			ORDER BY year
 		 ) b, aggregate_portfolio ag1, aggregate_portfolio ag2,
 			day_to_day dtd1, day_to_day dtd2
 	WHERE   dtd1.strategy_id = {0}
 			AND dtd2.strategy_id = dtd1.strategy_id
 			AND dtd1.portfolio_id = ag1.portfolio_id
 			AND dtd2.portfolio_id = ag2.portfolio_id
 			AND ag1.time = b.start_time
 			AND ag2.time = b.end_time
 UNION ALL
 	SELECT 
 		ROUND((power((ag2.portfolio_value/ag1.portfolio_value), 
 			(365/(b.end_time - b.start_time)))-1)*100, 2) as returns,
 		CAST('Overall (Annualized)' as CHAR(20)) as year
 	FROM (
 			SELECT MIN(ag.time) as start_time, MAX(ag.time) as end_time
			FROM   aggregate_portfolio ag, day_to_day dtd
			WHERE ag.portfolio_id = dtd.portfolio_id
				AND dtd.strategy_id = {0}
 		 ) b, aggregate_portfolio ag1, aggregate_portfolio ag2,
 			day_to_day dtd1, day_to_day dtd2
 	WHERE   dtd1.strategy_id = {0}
 			AND dtd2.strategy_id = dtd1.strategy_id
 			AND dtd1.portfolio_id = ag1.portfolio_id
 			AND dtd2.portfolio_id = ag2.portfolio_id
 			AND ag1.time = b.start_time
 			AND ag2.time = b.end_time

