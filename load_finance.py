
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
def insert_data(table,csv_name,cursor,db):
	with open( csv_name, 'r') as csvfile:
		data_reader = csv.reader(csvfile)
		for row in data_reader:
			row.insert(0,str(csv_name))
			row.append('NULL')
			row.append('NULL')
			sql_insert = "INSERT INTO {} VALUES {}".format(table,tuple(row))
			print sql_insert
			cursor.execute(sql_insert)
			db.commit()
			

if __name__ == '__main__':
	# Catching argv variables
	table = str(argv[1])
	csv_file = str(argv[2])

	db,cursor = connect()
	insert_data(table,csv_file,cursor,db)

	close(cursor,db)
