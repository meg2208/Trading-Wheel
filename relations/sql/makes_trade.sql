CREATE TABLE makes_trade (
	portfolio_id INTEGER,
	trade_id INTEGER,
	PRIMARY KEY(portfolio_id,trade_id),
	FOREIGN KEY (trade_id) REFERENCES trade,
	FOREIGN KEY (portfolio_id) REFERENCES current_portfolio
);
