CREATE TABLE portfolio_statistics (
	version INTEGER,
	sharpe_ratio REAL,
	returns REAL,
	user_id CHAR(20),
	PRIMARY KEY(user_id, version),
	FOREIGN KEY (user_id) REFERENCES user_data
);