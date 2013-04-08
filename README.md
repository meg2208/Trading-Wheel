Trading-Wheel
=============

Spring coms4111 Project by Nate Brennand and Matt Garbis.

Utilizes a SQL*Plus database and the web server is running the Python Flask framework.

[Various SQL*Plus queries](queries/explanation.md)

Explanation of sample strategy:
================================

The strategy will allocate 100% of a portfolio (starting with 100 dollars) to GOOG 
and 0% to cash when the 50 day moving average of GOOG crosses over (becomes higher than) 
the 200 day moving average of GOOG. It allocates 0% of the portolfio to GOOG and 100% to 
cash when the 50 day moving average of GOOG crosses below the 200 day moving average of GOOG.

We use sql queries to determine mva values and the date that they cross over/under.


Indicator:
	-- in schema change "field_data" to two separate attributes: "10_day_mva" and "25_day_mva"
	-- only one of the two attributes above are populated for each indicator 
	-- the left indicator is compared to the right indicator


