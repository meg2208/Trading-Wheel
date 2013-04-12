
from sys import argv
from decimal import Decimal
import cx_Oracle as oracle
import urllib2
from credentials import username, password, server


# Returns connections to the db and cursor objects
def connect():
    db = oracle.connect("{}/{}@{}".format(username, password, server))
    cursor = db.cursor()
    return db, cursor


# Closes the db and cursor connections
def close(db, cursor):
    cursor.close()
    db.close()


# Checks to see if a ticker has been uploaded into the table
def check_if_exists(ticker_symbol, cursor):
    sql_query = 'SELECT DISTINCT security FROM query_data'
    cursor.execute(sql_query)
    for security in cursor.fetchall():
        if ticker_symbol.upper() in str(security[0]):
            print 'Already loaded!'
            return True
    return False


# Expects YYYY-MM-DD
# Outputs DD-MMM-YYYY
def format_date(date_str):
    # DD-MMM-YYYY
    cal = [None, 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
           'sep', 'oct', 'nov', 'dec']
    date_split = date_str.split('-')
    date = [date_split[2], cal[int(date_split[1])], date_split[0]]
    date = '-'.join(date)
    return date


# Downloads from  yahoo
# Uploads to SQL*Plus
def get_data(ticker_symbol, db, cursor):
    url = "http://ichart.finance.yahoo.com/table.csv?s="+ticker_symbol
    counter = 0
    try:
        yahoo_data = urllib2.urlopen(url)
        for row in yahoo_data.readlines():
            if row[0:4] != 'Date':
                row = row.split(',')
                data = '(\'{}\',\'{}\',{},{},{},{},{},{},{},{})'.format(
                    ticker_symbol,          # security symbol
                    format_date(row[0]),    # date
                    Decimal(row[1]),        # open
                    Decimal(row[2]),        # high
                    Decimal(row[3]),        # low
                    Decimal(row[4]),        # close
                    int(row[5]),            # volume
                    Decimal(row[6]),        # adj_close
                    'NULL',                 # 10 day mva
                    'NULL'                  # 25 day mva
                )
                sql_insert = 'INSERT INTO query_data VALUES '+data
                print sql_insert
                cursor.execute(sql_insert)
                db.commit()
                counter += 1

    except urllib2.URLError as e:
        print e

    print counter, 'rows added'


# Callable method for module
def upload_ticker(ticker):
    ticker = str(ticker)
    ticker = ticker.encode('ascii', 'ignore')  # trying to remove non-ascii
    print 'someone tried to UPLOAD', ticker
    ticker - ticker.upper()
    db, cursor = connect()
    if check_if_exists(ticker, cursor) is False:
        get_data(ticker.upper(), db, cursor)
    close(db, cursor)


# Main method for command line testing
if __name__ == '__main__':
    if len(argv) != 2:
        print '\tProper Usage:\npython loader_finance.py <ticker name>'
        exit(1)
    ticker_name = str(argv[1]).upper()

    db, cursor = connect()
    if check_if_exists(ticker_name, cursor) is False:
        get_data(ticker_name, db, cursor)
    close(db, cursor)
