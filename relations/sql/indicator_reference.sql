CREATE TABLE indicator_reference(
	trigger_id INTEGER,
	strategy_id INTEGER,
	action_security CHAR(6),
	buy_sell CHAR(1),	--'Y' or 'N'
	operator char(10),
	share_amount INTEGER,
	allocation NUMBER,
	cash_value NUMBER,
	-- The user uses the reference
	indicator_id INTEGER,
	PRIMARY KEY (trigger_id),
	FOREIGN KEY (strategy_id, indicator_id, 'Y') REFERENCES indicator,
	FOREIGN KEY (strategy_id, indicator_id, 'N') REFERENCES indicator
);