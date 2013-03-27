CREATE TABLE indicator(
	indicator_id INTEGER,
	start_time DATE,	-- DD-MMM-YYYY
	end_time DATE,		-- DD-MMM-YYYY
	security CHAR(6),
	mva_50_day CHAR(1),
	mva_200_day CHAR(1),
	PRIMARY KEY (indicator_id)
);
