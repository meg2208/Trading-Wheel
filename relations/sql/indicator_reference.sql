CREATE TABLE indicator_reference(
	action_security CHAR(6),
	buy_sell CHAR(1),	--'Y' or 'N'
	operator char(10),
	share_amount INTEGER,
	allocation NUMBER,
	cash_value NUMBER,
	L_indicator_id INTEGER,
	R_indicator_id INTEGER,
	PRIMARY KEY (L_indicator_id,R_indicator_id),
	FOREIGN KEY (L_indicator_id) REFERENCES indicator,
	FOREIGN KEY (R_indicator_id) REFERENCES indicator
);
