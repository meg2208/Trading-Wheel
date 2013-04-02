CREATE TABLE trade(
	trade_id INTEGER,
	security CHAR(6),
	buy_sell CHAR(1),	--'B' or 'S'
	share_amount NUMBER,	-- Shares purchased in this trade
	price NUMBER,
	time DATE,
	portfolio_value NUMBER, -- current cash + value of securites in market
	securites_value NUMBER,	-- value of all securites in portfolio
	free_cash NUMBER,		-- cash not invested
	num_shares INTEGER,		-- # of shares currently owned
	PRIMARY KEY (trade_id)
);
