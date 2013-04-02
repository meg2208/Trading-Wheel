CREATE TABLE current_portfolio (
	trade_id INTEGER,
	portfolio_id INTEGER,
	PRIMARY KEY (trade_id,portfolio_id),
	trade_id REFERENCES trade,
	portfolio_id REFERENCES portfolio_at_trade
);
