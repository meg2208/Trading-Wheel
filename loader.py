
from sys import argv
import csv
import cx_Oracle as oracle
from credentials import username,password,server

# Catching argv variables
table = argv[1]
csv_file = argv[2]

# Connecting to oracle database
db = oracle.connect(username,password,server)
cursor = db.cursor()

# Reading in csv file contents
with open( csv_file, 'r') as csvfile:
	data_reader = csv.reader(csvfile)
	for row in data_reader:
		sql_insert = """BEGIN 
			INSERT INTO {} VALUES {}; 
			END;""".format(table,tuple(row))
		print sql_insert
		cursor.execute(sql_insert)
		db.commit()


cursor.close()
db.close()


