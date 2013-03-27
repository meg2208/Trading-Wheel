CREATE TABLE indicator(
	strategy_id INTEGER,
	start_time DATE,	-- DD-MMM-YYYY
	end_time DATE,		-- DD-MMM-YYYY
	security CHAR(6),
	indicator_id INTEGER,
	-- Can only be 'Y' or 'N'
	preceding_operator CHAR(1),
	-- tells which data to compare ('Y' or 'N')
	mva_50_day CHAR(1),
	mva_200_day CHAR(1),
	PRIMARY KEY (strategy_id, indicator_id, preceding_operator),
	FOREIGN KEY (strategy_id) references strategy
);
