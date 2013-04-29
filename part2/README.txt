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
    nsb2142 on ADB3


SCHEMA DECISIONS:
    We added the Analysis table to our schema to allow simple queries to compare user strategies against industry benchmarks. This would allow us to in bring in aspects of modern portfolio theory (wikipedia.org/wiki/Modern_portfolio_theory) to give users a better grasp of the effectiveness of their financial strategy.
    

"BENCHMARK_CONTENTS_TYPE"
    Each instance represents one holding in the total benchmark. Instantiated with strat_id, security, and allocation as parameters to constructor.

"BENCHMARK_VALUES"
    Contains the aggregate contents of the benchmark.  Total value is calculated upon initialization. Parameters: VARRAY of BENCHMARK_CONTENTS_TYPE, time

"HELPER"
Simply populates the portfolio_value and risk_free_rate in the analysis relation. Parameters: time, strat_id, analysis_id

SQL files for creation of the types can be found here:
https://github.com/nsb2142/Trading-Wheel/tree/master/types


QUERY EXPLANATIONS:
    annual returns:
        Returns a table consisting of your returns by year.
    
    
    

