MERGE INTO aggregate_portfolio A
		USING (
		select s.start_value as start_cash, s.start_value as start_port, 0 as start_sec, s.strategy_id, ag.portfolio_id, time
			FROM day_to_day dtd, aggregate_portfolio ag, strategy s
			WHERE ag.portfolio_id = dtd.portfolio_id
				AND s.strategy_id = dtd.strategy_id
				AND dtd.strategy_id = {0}
				AND time = (SELECT min(time)
					from day_to_day dtd1, aggregate_portfolio ag1, strategy s1
					where ag1.portfolio_id = dtd1.portfolio_id
						AND s1.strategy_id = dtd1.strategy_id
						AND s1.strategy_id = s.strategy_id)
		) B
		ON (B.portfolio_id = A.portfolio_id)
		WHEN MATCHED THEN UPDATE SET A.free_cash = B.start_cash, A.securites_value = B.start_sec, A.portfolio_value = B.start_port