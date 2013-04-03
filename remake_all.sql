DROP TABLE calculate_statistics;
DROP TABLE create_strategy;
DROP TABLE criteria;
DROP TABLE day_to_day;
DROP TABLE indicator_reference;
DROP TABLE makes_trade;
DROP TABLE portfolio_contents;
DROP TABLE raw_data_parsing;
DROP TABLE user_data;
DROP TABLE trade;
DROP TABLE strategy;
DROP TABLE security_state;
DROP TABLE query_data;
DROP TABLE portfolio_statistics;
DROP TABLE indicator;
DROP TABLE aggregate_portfolio;
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
	time DATE,
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
CREATE TABLE aggregate_portfolio(
	portfolio_id INTEGER,
	time DATE,				-- DD-MMM-YYYY
	portfolio_value NUMBER, -- current cash + value of securites in market
	interest_rate NUMBER,	-- interest paid on the cash held
	securites_value NUMBER,	-- value of all securites in portfolio
	free_cash NUMBER,		-- cash not invested
	portfolio_value_change NUMBER,	-- day to day change in value
	PRIMARY KEY (portfolio_id)
);
CREATE TABLE calculate_statistics (
	port_id INTEGER,
	strategy_id INTEGER,
	PRIMARY KEY (port_id),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (port_id) REFERENCES portfolio_statistics
);
CREATE TABLE create_strategy (
	user_id CHAR(20),
	strategy_id INTEGER,
	PRIMARY KEY (user_id, strategy_id ),
	FOREIGN KEY (user_id) REFERENCES user_data,
	FOREIGN KEY (strategy_id) REFERENCES strategy
);
CREATE TABLE criteria (
	strategy_id INTEGER,
	indicator_id INTEGER,
	PRIMARY KEY (strategy_id, indicator_id),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (indicator_id) REFERENCES indicator
);
CREATE TABLE day_to_day (
	strategy_id INTEGER,
	portfolio_id INTEGER,
	PRIMARY KEY (strategy_id, portfolio_id),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (portfolio_id) 	REFERENCES current_portfolio 
);
CREATE TABLE indicator_reference(
	L_indicator_id INTEGER,
	R_indicator_id INTEGER,
	buy_sell CHAR(1),	--'B' or 'S'
	operator CHAR(10),
	share_amount INTEGER,	--NULL
	allocation NUMBER,		--100
	cash_value NUMBER,
	PRIMARY KEY (L_indicator_id,R_indicator_id,buy_sell),
	FOREIGN KEY (L_indicator_id) REFERENCES indicator,
	FOREIGN KEY (R_indicator_id) REFERENCES indicator
);
CREATE TABLE makes_trade (
	portfolio_id INTEGER,
	trade_id INTEGER,
	PRIMARY KEY(portfolio_id,trade_id),
	FOREIGN KEY (trade_id) REFERENCES trade,
	FOREIGN KEY (portfolio_id) REFERENCES current_portfolio
);
CREATE TABLE portfolio_contents (
	state_id INTEGER,
	portfolio_id INTEGER,
	PRIMARY KEY (state_id, portfolio_id),
	FOREIGN KEY (state_id) REFERENCES security_state,
	FOREIGN KEY (portfolio_id) REFERENCES aggregate_portfolio,
);
CREATE TABLE raw_data_parsing (
	strategy_id INTEGER,
	security CHAR(6),
	time DATE,
	PRIMARY KEY (strategy_id, security,time),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (security, time) REFERENCES query_data
);
