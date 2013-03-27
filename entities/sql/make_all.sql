CREATE TABLE user_data(
	user_id CHAR(20),
	password CHAR(20),
	PRIMARY KEY (user_id)
);
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
CREATE TABLE strategy(
	strategy_id INTEGER,
	strategy_name CHAR(20),
	PRIMARY KEY (strategy_id)
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
	mva_50_day NUMBER,
	mva_200_day NUMBER,
	PRIMARY KEY (security, time)
);
CREATE TABLE portfolio_statistics (
	port_id INTEGER,
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
	mva_50_day CHAR(1),
	mva_200_day CHAR(1),
	PRIMARY KEY (indicator_id)
);
