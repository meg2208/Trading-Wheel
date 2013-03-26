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
	-- Shows which indicator is on which side ('Y' or 'N')
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
