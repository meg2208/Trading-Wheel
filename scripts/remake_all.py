
from os import system

entities = [
	"user_data",
	"trade",
	"strategy",
	"security_state",
	"query_data",
	"portfolio_statistics",
	"indicator",
	"aggregate_portfolio"]

relations = [
	"calculate_statistics",
	"create_strategy",
	"criteria",
	"day_to_day",
	"indicator_reference",
	"makes_trade",
	"portfolio_contents",
	"raw_data_parsing"]

with open("remake_all.sql",'w+') as f:

	for table in relations:
		f.write( "DROP TABLE {};\n".format( table ))


	for table in entities:
		f.write( "DROP TABLE {};\n".format( table ) )

	
	for table in entities:
		with open( "entities/sql/{}.sql".format(table), 'r' ) as entity_sql:
			for line in entity_sql:
				f.write( line )

	for table in relations:
		with open( "relations/sql/{}.sql".format(table), 'r' ) as relation_sql:
			for line in relation_sql:
				f.write( line )

