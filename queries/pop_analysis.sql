INSERT 
INTO analysis (analysis_id,
	start_date,
	end_date,
	time,
	strategy_id,
	risk_free_rate,
	portfolio_value,
	bench_values,
    help_obj)
SELECT seq_analysis_id.NextVal, 
		NULL as start_date, 
		NULL as end_date, 
		a.time as time, 
		a.strategy_id as strategy_id, 
		0 as risk_free_rate, 
		0 as portfolio_value, 
		BENCHMARK_VALUES(CONTENTS_LIST(
			BENCHMARK_CONTENTS_TYPE(a.strategy_id, 'BND', .4), 
			BENCHMARK_CONTENTS_TYPE(a.strategy_id, 'SPY', .6)), 
			a.time) as bench_values, 
		NULL as help_obj
FROM 	(SELECT DISTINCT ag.time, dtd.strategy_id 
		FROM   aggregate_portfolio ag, day_to_day dtd
		WHERE 	dtd.strategy_id = 1066
			AND dtd.portfolio_id = ag.portfolio_id
		ORDER BY ag.time) a;