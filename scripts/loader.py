
from sys import argv
import csv
import cx_Oracle as oracle
from credentials import username,password,server

# Connecting to oracle database
def connect():
	db = oracle.connect("{}/{}@{}".format(username,password,server))
	cursor = db.cursor()
	return db,cursor

def close(cursor,db):
	cursor.close()
	db.close()

def get_columns(table,cursor):
	sql_desc = "SELECT * FROM {} WHERE 1=0".format(table)
	cursor.execute(sql_desc)
	description = cursor.description
	columns = []
	for c in description:
		columns.append(c[0])
	print columns

def user_data(row):
	return tuple(row)

def strategy(row):
	return '({},\'{}\')'.format(row[0],row[1])

def indicator(row):
	return '({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(
		row[0],row[1],row[2],row[3],row[4],row[5])



# Reading in csv file contents
def insert_data(table,data,cursor,db):
	with open( data, 'r') as csvfile:
		data_reader = csv.reader(csvfile)
		for row in data_reader:
			sql_insert = "INSERT INTO {} VALUES {}".format(table,use(row))
			print sql_insert
			cursor.execute(sql_insert)
			db.commit()


if __name__ == '__main__':
	if len(argv) != 3:
		print 'Proper Usage:\n\tpython loader.py <table_name> <csv_file_name>' 
		exit(1)
	# Catching argv variables
	table = str(argv[1])
	use=user_data
	if table=='strategy':
		use = strategy

	csv_file = str(argv[2])

	db,cursor = connect()

	get_columns(table,cursor)

	insert_data(table,csv_file,cursor,db)

	close(cursor,db)
