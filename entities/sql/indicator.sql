CREATE TABLE indicator(
	strategy_id INTEGER,
	start_time DATE,
	end_time DATE,
	security CHAR(6),
	indicator_id INTEGER,
	-- Can only be 'Y' or 'N'
	preceding_operator CHAR(1),
	PRIMARY KEY (strategy_id, indicator_id)
	FOREIGN KEY (strategy_id) references strategy
);

