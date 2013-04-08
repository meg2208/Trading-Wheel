
from sys import argv
import cx_Oracle as oracle
from credentials import username,password,server

def connect():
    db = oracle.connect("{}/{}@{}".format(username,password,server))
    cursor = db.cursor()
    return db,cursor

def close(db,cursor):
    cursor.close()
    db.close()

def update_mva(ticker,ref,mva,num):
	db,cursor = connect()

	with file('queries/mva_mod.sql','r') as update:
		sql_update = update.read().format("'"+ticker+"'",ref,mva,num)
		cursor.execute( sql_update )
		db.commit()
		
	close(db,cursor)

if __name__ == '__main__':

	if len(argv) != 5:
		print 'Proper Usage:\n\tpython query_mva.py <ticker> <reference> <reference_mva> <# days>'
		exit(1)



	ticker = argv[1]
	reference = argv[2]
	mva = argv[3]
	num_days = argv[4]

	update_mva(ticker,reference,mva,num_days)
	exit(0)
	