INSERT INTO RAW_DATA_PARSING (strategy_id, security, time) 
	SELECT {0}, q.security, q.time
	FROM indicator_reference ir, criteria c,
		criteria c1, query_data q
	WHERE 
		q.time >= ir.start_time AND
		q.time <= ir.end_time AND
		ir.buy_sell = {1} AND
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
				AND r1.time = q.time)