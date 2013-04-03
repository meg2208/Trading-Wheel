CREATE TABLE portfolio_contents (
	state_id INTEGER,
	portfolio_id INTEGER,
	PRIMARY KEY (state_id, portfolio_id),
	FOREIGN KEY (state_id) REFERENCES security_state,
	FOREIGN KEY (portfolio_id) REFERENCES aggregate_portfolio,
);
