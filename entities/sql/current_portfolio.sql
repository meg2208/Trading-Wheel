CREATE TABLE current_portfolio(
	portfolio_id INTEGER,
	time DATE,				-- DD-MMM-YYYY
	portfolio_value NUMBER, -- current cash + value of securites in market
	interest_rate NUMBER,	-- interest paid on the cash held
	securites_value NUMBER,	-- value of all securites in portfolio
	free_cash NUMBER,		-- cash not invested
	portfolio_value_change NUMBER,	-- day to day change in value
	PRIMARY KEY (portfolio_id)
);
