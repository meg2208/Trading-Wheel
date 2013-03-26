CREATE TABLE query_data (
	security CHAR(6),
	time DATE, 	-- DD-MMM-YYYY
	open NUMBER,
	high NUMBER,
	low NUMBER,
	close NUMBER,
	volume INTEGER,
	adj_close NUMBER,
	-- field_data char(10) changed to...
	fifty_day_mva NUMBER,
	two_hundred_day_mva NUMBER,
	PRIMARY KEY (security, time)
);
