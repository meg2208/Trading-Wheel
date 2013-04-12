INSERT ALL 
	INTO aggregate_portfolio
		VALUES(seq_portfolio_id.nextval, time, 0, .03, 0,
			0, 0)
	INTO DAY_TO_DAY
		VALUES({0}, seq_portfolio_id.currval)
	SELECT DISTINCT time, strategy_id
		FROM (raw_data_parsing rd)
		WHERE rd.strategy_id = {0}