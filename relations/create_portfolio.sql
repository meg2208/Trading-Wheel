CREATE TABLE create_portfolio (
	strategy_id INTEGER,
	version INTEGER,
	user_id CHAR(20),
	PRIMARY KEY (strategy_id, user_id, version),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (user_id, version) REFERENCES portfolio_statistics
);