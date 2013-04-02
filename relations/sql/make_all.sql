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
CREATE TABLE raw_data_parsing (
	strategy_id INTEGER,
	security CHAR(6),
	time DATE,
	PRIMARY KEY (strategy_id, security,time),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (security, time) REFERENCES query_data
);
