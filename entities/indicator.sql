CREATE TABLE indicator(
	field_data CHAR(10),
	start_time DATE,
	end_time DATE,
	security CHAR(6),
	indicator_id INTEGER,
	PRIMARY KEY (indicator_id)
);