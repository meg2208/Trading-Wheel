CREATE TABLE indicator_reference(
	L_indicator_id INTEGER,
	R_indicator_id INTEGER,
	buy_sell CHAR(1),	--'B' or 'S'
	operator CHAR(10),
	share_amount INTEGER,
	allocation NUMBER,
	cash_value NUMBER,
	PRIMARY KEY (L_indicator_id,R_indicator_id,buy_sell),
	FOREIGN KEY (L_indicator_id) REFERENCES indicator,
	FOREIGN KEY (R_indicator_id) REFERENCES indicator
);
