CREATE TABLE trade (
	trade_id INTEGER,
	security CHAR(6),
	buy_sell CHAR(1),	--'B' or 'S'
	share_amount NUMBER,	-- Shares purchased in this trade
	price NUMBER,
	PRIMARY KEY(trade_id)
);
