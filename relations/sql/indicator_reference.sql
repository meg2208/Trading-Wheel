CREATE TABLE indicator_reference(
	action_security CHAR(6),
	-- BOOLEAN: Must be 'Y' or 'N'
	buy_sell CHAR(1),
	operator char(10),
	share_amount INTEGER,
	allocation REAL,
	cash_value REAL,
	-- The user uses the reference
	indicator_1 INTEGER,
	indicator_2 INTEGER,
	-- Shows which indicator is on which side
	preceding_operator_1 CHAR(1),
	preceding_operator_2 CHAR(1),
	PRIMARY KEY (indicator_1, indicator_2),
	FOREIGN KEY (indicator_1,preceding_operator_1) REFERENCES indicator,
	FOREIGN KEY (indicator_2,preceding_operator_2) REFERENCES indicator
);
