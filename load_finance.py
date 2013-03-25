
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

# Reading in csv file contents
def insert_data(csv_name,cursor,db):
	ticker = csv_name.split('/')[-1]
	ticker = ticker.split('/')[0]
	with open( csv_name, 'r') as csvfile:
		data_reader = csv.reader(csvfile)
		for row in data_reader:
			row.insert(0,str(csv_name))
			row.append('NULL')
			row.append('NULL')
			sql_insert = "INSERT INTO query_data VALUES {}".format(tuple(row))
			print sql_insert
			cursor.execute(sql_insert)
			db.commit()

if __name__ == '__main__':
	if len(argv) != 2:
		print '\tProper Usage:\npython loader_finance.py <ticker.csv>' 
		exit(1)

	# Catching argv variables
	csv_file = str(argv[1])

	db,cursor = connect()
	insert_data(csv_file,cursor,db)

	close(cursor,db)
