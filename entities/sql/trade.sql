CREATE TABLE trade (
	trade_id INTEGER,
	security CHAR(6),
	buy_sell CHAR(1),
	share_amount NUMBER,
	price NUMBER,
	time DATE,
	portfolio_value REAL,
	PRIMARY KEY (trade_id)
);
