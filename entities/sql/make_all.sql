CREATE TABLE user_data(
	user_id CHAR(20),
	password CHAR(20),
	PRIMARY KEY (user_id)
);
CREATE TABLE trade (
	trade_id INTEGER,
	security CHAR(6),
	buy_sell CHAR(1),	--'B' or 'S'
	share_amount NUMBER,	-- Shares purchased in this trade
	price NUMBER,
	PRIMARY KEY(trade_id)
);
CREATE TABLE strategy(
	strategy_id INTEGER,
	strategy_name CHAR(20),
	PRIMARY KEY (strategy_id)
);
CREATE TABLE security_state (
	state_id INTEGER,
	security CHAR(6),
	security_price NUMBER,
	share_amount NUMBER,
	PRIMARY KEY(state_id,security)
);
CREATE TABLE query_data (
	security CHAR(6),
	time DATE, 	-- DD-MMM-YYYY
	open NUMBER,
	high NUMBER,
	low NUMBER,
	close NUMBER,
	volume INTEGER,
	adj_close NUMBER,
	-- field_data char(10) changed to...
	mva_10_day NUMBER,
	mva_25_day NUMBER,
	PRIMARY KEY (security, time)
);
CREATE TABLE portfolio_statistics (
	port_id INTEGER,
	start_date DATE,
	end_date DATE,
	sharpe_ratio REAL,
	returns REAL,
	user_id CHAR(20),
	PRIMARY KEY(port_id)
);
CREATE TABLE indicator(
	indicator_id INTEGER,
	start_time DATE,	-- DD-MMM-YYYY
	end_time DATE,		-- DD-MMM-YYYY
	security CHAR(6),
	mva_10_day CHAR(1),
	mva_25_day CHAR(1),
	PRIMARY KEY (indicator_id)
);
CREATE TABLE current_portfolio(
	portfolio_id INTEGER,
	time DATE,				-- DD-MMM-YYYY
	portfolio_value NUMBER, -- current cash + value of securites in market
	interest_rate NUMBER,	-- interest paid on the cash held
	securites_value NUMBER,	-- value of all securites in portfolio
	free_cash NUMBER,		-- cash not invested
	portfolio_value_change NUMBER,	-- day to day change in value
	PRIMARY KEY (portfolio_id)
);
