CREATE TABLE indicator_reference(
	trigger_id INTEGER,
	strategy_id INTEGER,
	action_security CHAR(6),
	-- BOOLEAN: Must be 'Y' or 'N'
	buy_sell CHAR(1),
	operator char(10),
	share_amount INTEGER,
	allocation NUMBER,
	cash_value NUMBER,
	-- The user uses the reference
	indicator_id INTEGER,
	PRIMARY KEY (trigger_id),
	FOREIGN KEY (strategy_id, indicator_id) REFERENCES criteria
);