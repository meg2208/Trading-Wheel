CREATE TABLE action (
	strategy_id INTEGER,
	trade_id INTEGER,
	PRIMARY KEY (strategy_id, trade_id),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (trade_id) REFERENCES trade
);