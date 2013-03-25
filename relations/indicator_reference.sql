CREATE TABLE indicator_reference(
	action_security CHAR(6),
	-- BOOLEAN: Must be 'Y' or 'N'
	buy_sell CHAR(1),
	operator char(10),
	share_amount INTEGER,
	allocation REAL,
	cash_value REAL,
	indicator_user INTEGER,
	-- The user uses the reference
	indicator_ref INTEGER,
	PRIMARY KEY (indicator_user, indicator_ref),
	FOREIGN KEY (indicator_user) REFERENCES indicator,
	FOREIGN KEY (indicator_ref) REFERENCES indicator
);