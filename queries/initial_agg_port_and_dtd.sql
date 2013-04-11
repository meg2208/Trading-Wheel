--first step after set_rdp_relation
--creates initial aggregate_portfolio rows and day_to_day relations
INSERT ALL 
	INTO aggregate_portfolio
		VALUES(seq_portfolio_id.nextval, time, 0, .03, 0,
			0, 0)
	INTO DAY_TO_DAY
		VALUES(1000, seq_portfolio_id.currval)
	SELECT DISTINCT time, strategy_id
		FROM (raw_data_parsing rd)
		WHERE rd.strategy_id = {0}; --make modular