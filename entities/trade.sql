CREATE TABLE trade (
	trade_id INTEGER,
	buy_sell CHAR(1),
	security CHAR(6),
	time DATE,
	portfolio_value REAL,
	PRIMARY KEY (trade_id)
);