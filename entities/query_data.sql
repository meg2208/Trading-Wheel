CREATE TABLE query_data (
	time DATE,
	security CHAR(6),
	field_data char(10),
	PRIMARY KEY (security, field_data)
);