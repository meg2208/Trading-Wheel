
from sys import argv
import csv
import cx_Oracle as oracle
from credentials import username,password,server

# Connecting to oracle database
def connect():
    db = oracle.connect("{}/{}@{}".format(username,password,server))
    cursor = db.cursor()
    return db,cursor

def close(db,cursor):
    cursor.close()
    db.close()

def get_columns(cursor):
    sql_desc = "SELECT * FROM {} WHERE 1=0".format(argv[1])
    cursor.execute(sql_desc)
    description = cursor.description
    columns = []
    for c in description:
        columns.append(c[0])
    print columns

# DD-MMM-YYYY
def format_date(date_str):
    cal = [None,'jan','feb','mar','apr','may','jun','jul','aug','sep',
        'oct','nov','dec']
    date_split = date_str.split('-')
    date = [date_split[1], cal[int(date_split[0])], date_split[2]]
    date = '-'.join(date)
    return date

# ENTITIES
def aggregate_portfolio(row):
    return '({},\'{}\',{},{},{},{},{})'.format(row[0],row[1],
       row[2],row[3],row[4],row[5],row[6])

def indicator(row):
    return '({},\'{}\',\'{}\',\'{}\')'.format(
        row[0],row[1],row[2],row[3])

def portfolio_statistics(row):
    return '({},{},{},\'{}\')'.format(row[0],row[1],row[2],row[3])

def query_data(row):
    print 'Use load_finance.py!'
    exit(1)

def security_state(row):
    return '({},\'{}\',{},{})'.format(row[0],row[1],row[2],row[3])

def strategy(row):
    return '({},\'{}\')'.format(row[0],row[1])

def trade(row):
    return '({},\'{}\',\'{}\',{},{},\'{}\')'.format(
        row[0],row[1],row[2],row[3],row[4],row[5])

def user_data(row):
    return '(\'{}\',\'{}\')'.format(row[0],row[1])

# RELATIONS
def calculate_statistics(row):
    return '({},{})'.format(row[0],row[1])

def create_strategy(row):
    return '(\'{}\',{})'.format(row[0],row[1])

def criteria(row):
    return '({},{})'.format(row[0],row[1])

def day_to_day(row):
    return '({},{})'.format(row[0],row[1])

def indicator_reference(row):
    return '(\'{}\',\'{}\',{},{},\'{}\',\'{}\',\'{}\',{},{},{})'.format(
        format_date(row[0]),format_date(row[1]),row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])    

def makes_trade(row):
    return '({},{})'.format(row[0],row[1])

def portfolio_contents(row):
    return '({},{},\'{}\')'.format(row[0],row[1],row[2])

def raw_data_parsing(row):
    return '({},\'{}\',\'{}\')'.format(
        row[0],row[1],format_date(row[2]))

def determine_table(name):
    converters = { 'calculate_statistics':calculate_statistics,
        'create_strategy':create_strategy,
        'criteria':criteria,
        'day_to_day':day_to_day,
        'indicator_reference':indicator_reference,
        'makes_trade':makes_trade,
        'portfolio_contents':portfolio_contents,
        'raw_data_parsing':raw_data_parsing,
        'aggregate_portfolio':aggregate_portfolio,
        'indicator':indicator,
        'portfolio_statistics':portfolio_statistics,
        'security_state':security_state,
        'query_data':query_data,
        'strategy':strategy,
        'trade':trade,
        'user_data':user_data
    }
    return converters[name]

def insert_data(table_name,data,db=None,cursor=None):
    #For single insert use
    close_at_end = False
    if db is None:
        db,cursor = connect()
        close_at_end = True

    use = determine_table(table_name)
    sql_insert = "INSERT INTO {} VALUES {}".format(table_name,use(data))
    print sql_insert
    cursor.execute(sql_insert)
    db.commit()

    if close_at_end:
        close(db,cursor)

# Reading in csv file contents
def insert_csv_data(csv_file):
    table_name = argv[1]
    db,cursor = connect()

    #print out columns
    get_columns(cursor)

    with open( csv_file, 'r') as csvfile:
        data_reader = csv.reader(csvfile)
        for row in data_reader:
            insert_data( argv[1], row, db, cursor)

    close(db,cursor)

# Main
if __name__ == '__main__':
    if len(argv) != 3:
        print 'Proper Usage:\n\tpython loader.py <table_name> <csv_file_name>' 
        exit(1)

    csv_file = str(argv[2])
    insert_csv_data(csv_file)
