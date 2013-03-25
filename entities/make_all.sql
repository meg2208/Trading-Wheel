CREATE TABLE user_data(
	user_id CHAR(20),
	password CHAR(20),
	PRIMARY KEY (user_id)
);
CREATE TABLE indicator(
	field_data CHAR(10),
	start_time DATE,
	end_time DATE,
	security CHAR(6),
	indicator_id INTEGER,
	PRIMARY KEY (indicator_id)
);
CREATE TABLE portfolio_statistics (
	version INTEGER,
	sharpe_ratio REAL,
	returns REAL,
	user_id CHAR(20),
	PRIMARY KEY(user_id, version),
	FOREIGN KEY (user_id) REFERENCES user_data
);
CREATE TABLE query_data (
	time DATE,
	security CHAR(6),
	field_data char(10),
	PRIMARY KEY (security, field_data)
);
CREATE TABLE strategy(
	strategy_id INTEGER,
	strategy_name CHAR(20),
	PRIMARY KEY (strategy_id)
);
CREATE TABLE trade (
	trade_id INTEGER,
	buy_sell CHAR(1),
	security CHAR(6),
	time DATE,
	portfolio_value REAL,
	PRIMARY KEY (trade_id)
);
