import urllib2
import sys
import os

# queries for csv of historical stock data
# saves in users/... --> python import_hist_data.py /users/whateveryouwant aapl goog
# saves in current dir -->  python import_hist_data.py aapl goog

base_url = "http://ichart.finance.yahoo.com/table.csv?s="
contains_dir = False

# Checks securites folder for csv file with matching ticker
def check_if_exists(ticker_symbol):
    for security in os.listdir('entities/securities'):
        if security.split('.')[0].lower() == ticker_symbol.lower():
            return True
    return False

def make_url(ticker_symbol):
    return base_url + ticker_symbol

#puts files in current dir unless first arg is desired dir
def make_filename(ticker_symbol):
    file_path = "entities/securities/{}.csv".format(ticker_symbol)
    return file_path

def pull_historical_data(ticker_symbol):
    try:
        yahoo_data = urllib2.urlopen( make_url(ticker_symbol))
        first = True
        with file( make_filename(ticker_symbol), 'w+' ) as sec:
            for line in yahoo_data:
                if not first:
                    sec.write( line )
                first = False
    except URLError as e:
        print e

# 2nd, 3rd, ... args are stocks to query for
if __name__ == '__main__':
    for stock in sys.argv[1:]:
        if not check_if_exists( stock ):
            pull_historical_data( stock )

