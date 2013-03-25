Trading-Wheel
=============

COMS4111 Project

The "entities" file contains all of the SQL statements to create all of the entities.

The "relations" file contains all of the SQL statements to create all of the relations. 

SQL queries are for a 10g Oracle SQL Server.

Explanation of sample strategy:

Since this is a preliminary version, the buy and sell dates and values are arbitrarily chosen.  They are NOT chosen based on the real life indicator values (which will depend on sql queries for moving average).

The strategy will allocate 100% of a portfolio (starting with 100 dollars) to GOOG and 0% to cash when the 50 day moving average of GOOG crosses over (becomes higher than) the 200 day moving average of GOOG. It allocates 0% of the portolfio to GOOG and 100% to cash when the 50 day moving average of GOOG crosses below the 200 day moving average of GOOG.

We arbitrarily chose the dates where the moving averages cross over/under because the final version will determine the dates based on sql queries. 

Indicator:
	-- in schema change "field_data" to two separate attributes: "50_day_mva" and "200_day_mva"
	-- only one of the two attributes above are populated for each indicator 


