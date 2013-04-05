
from sys import argv
from decimal import Decimal
import cx_Oracle as oracle
import urllib2
from credentials import username,password,server

# Connecting to oracle database
def connect():
    db = oracle.connect("{}/{}@{}".format(username,password,server))
    cursor = db.cursor()
    return db,cursor

#Closing connections
def close(db,cursor):
    cursor.close()
    db.close()

def check_if_exists(ticker_symbol,cursor):
    sql_query = 'SELECT DISTINCT security FROM query_data'
    cursor.execute( sql_query )
    for security in cursor.fetchall():
        if ticker_symbol.upper() in str(security[0]):
            print 'Already loaded!'
            return True
    return False

# DD-MMM-YYYY
def format_date(date_str):
    cal = [None,'jan','feb','mar','apr','may','jun','jul','aug','sep',
        'oct','nov','dec']
    date_split = date_str.split('-')
    date = [date_split[2], cal[int(date_split[1])], date_split[0]]
    date = '-'.join(date)
    return date

def get_data(ticker_symbol,db,cursor):
    url = "http://ichart.finance.yahoo.com/table.csv?s="+ticker_symbol
    counter =  0
    try:
        yahoo_data = urllib2.urlopen( url )
        closing_10 = [0]*10
        closing_25 = [0]*25

        for line in reversed(yahoo_data.readlines()):
            if line[0:4] != 'Date':
                row = line.split(',')

                closing_10[counter%10] = Decimal(row[4])
                if counter > 9:
                    mva_10_day = sum(closing_10)/10
                else:
                    mva_10_day = 'NULL'
                closing_25[counter%25] = Decimal(row[4])
                if counter > 24:
                    mva_25_day = sum(closing_25)/25
                else:
                    mva_25_day = 'NULL'

                data = '(\'{}\',\'{}\',{},{},{},{},{},{},{},{})'.format(
                    ticker_symbol,      # security symbol
                    format_date(row[0]),# date
                    Decimal(row[1]),    # open
                    Decimal(row[2]),    # high
                    Decimal(row[3]),    # low
                    Decimal(row[4]),    # close
                    int(row[5]),        # volume
                    Decimal(row[6]),    # adj_close
                    mva_10_day,         # 10 day mva
                    mva_25_day          # 25 day mva
                    )
                sql_insert = 'INSERT INTO query_data VALUES '+data
                print sql_insert
                cursor.execute(sql_insert)
                db.commit()
                counter += 1

    except urllib2.URLError as e:
        print e

    print counter,' rows added'       

def upload_ticker(ticker):
    ticker - ticker.upper()
    db,cursor = connect()
    if check_if_exists(ticker,cursor) is False:
        get_data(ticker.upper(),db,cursor)
    close(db,cursor)


if __name__ == '__main__':
    if len(argv) != 2:
        print '\tProper Usage:\npython loader_finance.py <ticker name>' 
        exit(1)
    ticker_name = str(argv[1]).upper()

    db,cursor = connect()
    if check_if_exists(ticker_name,cursor) is False:
        get_data(ticker_name,db,cursor)
    close(db,cursor)

