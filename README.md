Trading-Wheel
=============

COMS4111 Project

The "entities" file contains all of the SQL statements to create all of the entities.

The "relations" file contains all of the SQL statements to create all of the relations. 

SQL queries are for a 10g Oracle SQL Server.

Explanation of sample strategy:
================================

The strategy will allocate 100% of a portfolio (starting with 100 dollars) to GOOG and 0% to cash when the 50 day moving average of GOOG crosses over (becomes higher than) the 200 day moving average of GOOG. It allocates 0% of the portolfio to GOOG and 100% to cash when the 50 day moving average of GOOG crosses below the 200 day moving average of GOOG.

We use sql queries to determine mva values and the date that they cross over/under.


Indicator:
	-- in schema change "field_data" to two separate attributes: "50_day_mva" and "200_day_mva"
	-- only one of the two attributes above are populated for each indicator 
	-- the left indicator is compared to the right indicator


