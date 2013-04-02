CREATE TABLE portfolio_at_trade (
	trade_id INTEGER,
	security CHAR(6),
	share_amount NUMBER,
	portfolio_id INTEGER,
	PRIMARY KEY(portfolio_id,trade_id)
);
