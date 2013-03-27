CREATE TABLE indicator(
	start_time DATE,	-- DD-MMM-YYYY
	end_time DATE,		-- DD-MMM-YYYY
	security CHAR(6),
	indicator_id INTEGER,
	mva_50_day CHAR(1),
	mva_200_day CHAR(1),
	PRIMARY KEY (indicator_id)
);
