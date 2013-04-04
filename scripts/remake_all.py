
# remake_all
#
# Reads in the contents of the entitites and relations sql folders.
# Uses these to create a master sql file that drops and remakes all
# tables from the database.
# Checks for len != 0 are to prevent DS_Store from being added.

import os

entities = []
for entity in os.listdir('entities/sql'):
	entity = entity.split('.')[0]
	if len(entity) != 0:
		entities.append( entity )

relations = []
for relation in os.listdir('relations/sql'):
	relation = relation.split('.')[0]
	if len(relation) != 0:
		relations.append( relation )

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

