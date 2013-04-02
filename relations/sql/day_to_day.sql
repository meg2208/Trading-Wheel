CREATE TABLE day_to_day (
	strategy_id INTEGER,
	portfolio_id INTEGER,
	PRIMARY KEY (strategy_id, portfolio_id),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (portfolio_id) 	REFERENCES current_portfolio 
);
