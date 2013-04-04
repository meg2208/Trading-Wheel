import urllib
import sys
import os

# querys for csv of historical stock data
# saves in users/... --> python import_hist_data.py /users/whateveryouwant aapl goog
# saves in current dir -->  python import_hist_data.py aapl goog

base_url = "http://ichart.finance.yahoo.com/table.csv?s="
contains_dir = False

def make_url(ticker_symbol):
    return base_url + ticker_symbol

#puts files in current dir unless first arg is desired dir
def make_filename(ticker_symbol):
	if sys.argv[0][0] == "/":
		contains_dir = True
		file_path = "/" + sys.argv[1] + "/" + ticker_symbol + ".csv"
	else:
		file_path = os.getcwd() + "/" + ticker_symbol + ".csv"
	return file_path

def pull_historical_data(ticker_symbol):
    try:
        urllib.urlretrieve(make_url(ticker_symbol), make_filename(ticker_symbol))
    except urllib.ContentTooShortError as e:
        outfile = open(make_filename(ticker_symbol, directory), "w")
        outfile.write(e.content)
        outfile.close()

# 2nd, 3rd, ... args are stocks to query for
if __name__ == '__main__':
	if contains_dir == True:
		for stocks in sys.argv[2:]:
			pull_historical_data(stocks)
	else:
		for stocks in sys.argv[1:]:
			pull_historical_data(stocks)