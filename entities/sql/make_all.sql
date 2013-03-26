CREATE TABLE user_data(
	user_id CHAR(20),
	password CHAR(20),
	PRIMARY KEY (user_id)
);
CREATE TABLE trade (
	trade_id INTEGER,
	buy_sell CHAR(1),
	security CHAR(6),
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
	50_day_mva NUMBER,
	200_day_mva NUMBER,
	PRIMARY KEY (security, time)
);
CREATE TABLE portfolio_statistics (
	version INTEGER,
	sharpe_ratio REAL,
	returns REAL,
	user_id CHAR(20),
	PRIMARY KEY(user_id, version),
	FOREIGN KEY (user_id) REFERENCES user_data
);
CREATE TABLE indicator(
	strategy_id INTEGER,
	start_time DATE,
	end_time DATE,
	security CHAR(6),
	indicator_id INTEGER,
	-- Can only be 'Y' or 'N'
	preceding_operator CHAR(1),
	-- tells which data to compare ('Y' or 'N')
	50_day_mva CHAR(1),
	200_day_mva CHAR(1),
	PRIMARY KEY (strategy_id, indicator_id, preceding_operator)
	FOREIGN KEY (strategy_id) references strategy
);

