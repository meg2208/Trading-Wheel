-- we use the objects to populate this relation
CREATE TABLE analysis (
	analysis_id NUMBER,
	start_date DATE,
	end_date DATE,
	time DATE,
--	frequency VARCHAR2(10), -- daily, monthly, yearly
	strategy_id NUMBER,
	risk_free_rate NUMBER,
	portfolio_value NUMBER,
	bench_values BENCHMARK_VALUES(contents CONTENTS_LIST, time DATE),
	help_obj HELPER(time DATE, strategy_id NUMBER),
	PRIMARY KEY (analysis_id, strategy_id),
	FOREIGN KEY (strategy_id) REFERENCES strategy
);

