CREATE TABLE indicator(
	start_time DATE,
	end_time DATE,
	security CHAR(6),
	indicator_id INTEGER,
	-- Can only be 'Y' or 'N'
	preceding_operator CHAR(1),
	PRIMARY KEY (indicator_id, preceding_operator)
);

