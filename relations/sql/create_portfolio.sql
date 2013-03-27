CREATE TABLE create_portfolio (
	strategy_id INTEGER,
	port_id INTEGER,
	PRIMARY KEY (port_id),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (port_id) REFERENCES portfolio_statistics
);
