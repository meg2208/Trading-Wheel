CREATE TABLE indicator(
	indicator_id INTEGER,
	start_time DATE,	-- DD-MMM-YYYY
	end_time DATE,		-- DD-MMM-YYYY
	security CHAR(6),
	mva_10_day CHAR(1),
	mva_25_day CHAR(1),
	PRIMARY KEY (indicator_id)
);
