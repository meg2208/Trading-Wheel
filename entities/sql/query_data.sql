CREATE TABLE query_data (
	security CHAR(6),
	time DATE,
	open NUMBER,
	high NUMBER,
	low NUMBER,
	close NUMBER,
	volume INTEGER,
	adj_close NUMBER,
	-- field_data char(10) changed to...
	50_day_mva NUMBER,
	200_day_mva NUMBER,
	PRIMARY KEY (security, time)
);
