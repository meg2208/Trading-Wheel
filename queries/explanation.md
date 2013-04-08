# SQL Queries
---------------



### All
This query returns all tables that are in the SQL*Plus database.

### Mine
This query returns the name of all of the tables created by the profile 'nsb2142'

### insert_ind_ref
Populates indicator reference relation. 

### mva_mod
Calculates and populates moving average of a security (first argument) for 
a variable in query_data (second argument), such as price or volume, over a 
given time period (fourth argument), and populates in a given column in 
query_data (third argument).

### x_over
Queries for date and price of the dates where, for a given security (first argument),
a data point in query_data (second argument) crosses over another data point in

### pop_temp_b_x_over 
This creates trade entities when an indicator_reference has a buy triggered by 
the 10 day mva crossing over 25 day moving average. It auto-generates the trade_id 
using a sql object called seq_tid in the db. It is temporary until the system 
determines that the portfolio has enough  cash to purchase the desired amount.  
*needs to be modified to also create a makes_trade relation.
*needs to be modified to be more modular.

### pop_temp_agg_portfolio [to be completed]
Creates an aggregate_portfolio for each day of the strategy. Also will create
a day_to_day relation for each day of the strategy. The first day is always 
determined by the cash_value amount in the indicator reference with the earliest
start_date.

### pop_final_portfolio [to be completed]
Iterates through all days of aggregate portfolio. 
If a makes_trade relation exists for a given day, 
  check the amount (or allocation) to designate to that security,
  then create/modify a security_state/aggregate_portfolio object to reflect the 
    correct balance of that security/portfolio and cash amt
    and link with a new portfolio_contents relation.
If no makes_trade relation exists, 
  for each security currently held
  (removing security_price as an attribute create security_state and portfolio_contents objects
  would take away the need for another row in security_state). 
    Then let portfolio_value = yesterdays_portfolio_value + 
        (yesterdays_share_price - share_price)*share_amount
portfolio_value_change = portfolio_value - yesterdays_portfolio_value

### set_rdp_relation
This associates the strategy with the proper securities and time periods by 
creating raw_data_parsing relationships. It is a necessary step after the 
indicator criteria and query_data has been filled.  The first argument is 
the strategy_id and second is 'B' or 'S'.  It should be run twice only 
if the strategy contains a set if indicator references where the buy and 
sell references have different action_securities.
