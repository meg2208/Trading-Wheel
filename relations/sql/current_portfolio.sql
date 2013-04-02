CREATE TABLE portfolio_securities(
	portfolio_id INTEGER,
	state_id INTEGER,
	PRIMARY KEY (portfolio_id,state_id),
	current_portfolio REFERENCES current_portfolio,
	state_id REFERENCES security_state
);
