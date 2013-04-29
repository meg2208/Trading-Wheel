Project 2

GROUP:
meg2208 - Matt Garbis
nsb2142 - Nate Brennand

FILES:
Schema transcript
    nsb2142-meg2208-project2.dmp
Queries file
    queries.txt

ORACLE ACCOUNT:
    nsb2142

SCHEMA DECISIONS:
new relation in db: Analysis

Analysis stores information (risk-free rate, benchmark returns) that is
useful for calculating MPT stats.

"BENCHMARK_CONTENTS_TYPE"
Each instance represents one holding in the total benchmark.
Instantiated with strat_id, security, and allocation as parameters to
constructor.

"BENCHMARK_VALUES"
Contains the aggregate contents of the benchmark.  Total value is
calculated upon initialization.
Parameters: VARRAY of BENCHMARK_CONTENTS_TYPE, time

"HELPER"
Simply populates the portfolio_value and risk_free_rate in the analysis
relation.
Parameters: time, strat_id, analysis_id

