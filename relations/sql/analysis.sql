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
	bench_values BENCHMARK_VALUES(VARRAY(10) OF BENCH_CONTENTS_TYPE, time),
	help_obj HELPER(time, strategy_id NUMBER),
	PRIMARY KEY (analysis_id, strategy_id),
	FOREIGN KEY (strategy_id) REFERENCES strategy
);

