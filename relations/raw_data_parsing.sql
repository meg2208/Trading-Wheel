CREATE TABLE raw_data_parsing (
	strategy_id INTEGER,
	security CHAR(6),
	field_data char(10),
	PRIMARY KEY (strategy_id, security),
	FOREIGN KEY (strategy_id) REFERENCES strategy,
	FOREIGN KEY (security, field_data) REFERENCES query_data
);