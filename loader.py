
from sys import argv
import csv
import cx_Oracle as oracle
from credentials import username,password,server

# Catching argv variables
table = argv[1]
csv = argv[2]

# Connecting to oracle database
connection = oracle.Connection(username,password,server)
cursor = oracle.cursor(connection)

# Reading in csv file contents
with open( csv, 'r') as csvfile:
	data_reader = csv.reader(csvfile)



cursor.close()
connection.close()


