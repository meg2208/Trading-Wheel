-- we use the objects to populate this relation
CREATE TABLE analysis (
	analysis_id NUMBER,
	start_date DATE,
	end_date DATE,
	time DATE,
	strategy_id NUMBER,
	risk_free_rate NUMBER,
	portfolio_value NUMBER,
	bench_values BENCHMARK_VALUES(strategy_id NUMBER, contents CONTENTS_LIST, time DATE, value NUMBER),
	PRIMARY KEY (analysis_id, strategy_id),
	CONSTRAINT s_fk FOREIGN KEY (strategy_id) REFERENCES strategy
);

