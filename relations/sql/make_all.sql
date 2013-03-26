CREATE TABLE action (
	strategy_id INTEGER,
	trade_id INTEGER,
	PRIMARY KEY (strategy_id, trade_id),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (trade_id) REFERENCES trade
);
CREATE TABLE create_portfolio (
	strategy_id INTEGER,
	version INTEGER,
	user_id CHAR(20),
	PRIMARY KEY (strategy_id, user_id, version),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (user_id, version) REFERENCES portfolio_statistics
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
CREATE TABLE indicator_reference(
	action_security CHAR(6),
	-- BOOLEAN: Must be 'Y' or 'N'
	buy_sell CHAR(1),
	operator char(10),
	share_amount INTEGER,
	allocation REAL,
	cash_value REAL,
	-- The user uses the reference
	indicator_id_1 INTEGER,
	indicator_id_2 INTEGER,
	-- Shows which indicator is preceding the operator ('Y' or 'N')
	-- Constraint: both cannot be equal
	preceding_operator_1 CHAR(1),
	preceding_operator_2 CHAR(1),
	-- tells which data to compare ('Y' or 'N')
	50_day_mva CHAR(1),
	200_day_mva CHAR(1),
	PRIMARY KEY (indicator_id_1, indicator_id_2),
	FOREIGN KEY (indicator_id_1,preceding_operator_1) REFERENCES indicator,
	FOREIGN KEY (indicator_id_2,preceding_operator_2) REFERENCES indicator
);
CREATE TABLE raw_data_parsing (
	strategy_id INTEGER,
	security CHAR(6),
	field_data char(10),
	PRIMARY KEY (strategy_id, security),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (security, field_data) REFERENCES query_data
);
