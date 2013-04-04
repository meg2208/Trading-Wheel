
from sys import argv
from decimal import Decimal
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

# DD-MMM-YYYY
def format_date(date_str):
    cal = [None,'jan','feb','mar','apr','may','jun','jul','aug','sep',
        'oct','nov','dec']
    date_split = date_str.split('-')
    date = [date_split[2], cal[int(date_split[1])], date_split[0]]
    date = '-'.join(date)
    return date

# Reading in csv file contents
def insert_data(csv_name,cursor,db):
    ticker = csv_name.split('/')[-1]
    ticker = ticker.split('.')[0]
    counter = 0
    with open( csv_name, 'r') as csvfile:
        data_reader = csv.reader(csvfile)
        for row in data_reader:
            data = '(\'{}\',\'{}\',{},{},{},{},{},{},{},{})'.format(
                ticker,				# security symbol
                format_date(row[0]),# date
                Decimal(row[1]),	# open
                Decimal(row[2]),    # high
                Decimal(row[3]),    # low
                Decimal(row[4]),    # close
                int(row[5]),        # volume
                Decimal(row[6]),    # adj_close
                'NULL',				# 10 day mva
                'NULL'				# 25 day mva
                )
            sql_insert = 'BEGIN INSERT INTO query_data \nVALUES '+data+'; END;';
            print sql_insert
            cursor.execute(sql_insert)
            db.commit()
            counter += 1
    print counter,' rows added'        

if __name__ == '__main__':
    if len(argv) != 2:
        print '\tProper Usage:\npython loader_finance.py <ticker.csv>' 
        exit(1)

    # Catching argv variables
    csv_file = str(argv[1])

    db,cursor = connect()
    insert_data(csv_file,cursor,db)

    close(cursor,db)
