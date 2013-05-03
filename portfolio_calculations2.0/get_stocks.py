
from sys import argv
from decimal import Decimal
import urllib2
from stock import Stock
from day_stock import Day_Stock


def get_data(ticker_symbol, mva_choices=None):
    url = "http://ichart.finance.yahoo.com/table.csv?s="+ticker_symbol
    counter = 0
    new_stock = Stock(ticker_symbol, mva_choices)

    try:
        yahoo_data = urllib2.urlopen(url)

        closing_prices = []
        for choice in mva_choices:
            closing_prices.append([choice, [0]*choice])

        for line in reversed(yahoo_data.readlines()):
            if line[0:4] != 'Date':  # skips header line
                row = line.split(',')

                mva = {}
                for interval in closing_prices:
                    interval[1][counter % interval[0]] = float(row[4])
                    if counter >= interval[0]-1:
                        mva[interval[0]] = sum(interval[1])/interval[0]
                    else:
                        mva[interval[0]] = None

                new_stock.days.append(Day_Stock(
                    row[0],                 # date
                    Decimal(row[1]),        # open
                    Decimal(row[2]),        # high
                    Decimal(row[3]),        # low
                    Decimal(row[4]),        # close
                    int(row[5]),            # volume
                    Decimal(row[6]),        # adj_close
                    mva                     # various moving averages
                ))
                print mva
                counter += 1

    except urllib2.URLError as e:
        print e

    print counter, ' rows added'
    return new_stock


if __name__ == '__main__':
    if len(argv) != 2:
        print 'Proper Usage:\n\tpython loader_finance.py <ticker name>'
        exit(1)
    ticker_name = str(argv[1]).upper()
