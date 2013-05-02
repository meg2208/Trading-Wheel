
from sys import argv
from decimal import Decimal
import urllib2


# DD-MMM-YYYY
def format_date(date_str):
    cal = [None, 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    date_split = date_str.split('-')
    date = [date_split[2], cal[int(date_split[1])], date_split[0]]
    date = '-'.join(date)
    return date


def get_data(ticker_symbol):
    url = "http://ichart.finance.yahoo.com/table.csv?s="+ticker_symbol
    counter = 0
    try:
        yahoo_data = urllib2.urlopen(url)
        closing_10 = [0]*10
        closing_25 = [0]*25

        for line in reversed(yahoo_data.readlines()):
            if line[0:4] != 'Date':
                row = line.split(',')

                closing_10[counter % 10] = Decimal(row[4])
                if counter > 9:
                    mva_10_day = sum(closing_10)/10
                else:
                    mva_10_day = 'NULL'
                closing_25[counter % 25] = Decimal(row[4])
                if counter > 24:
                    mva_25_day = sum(closing_25)/25
                else:
                    mva_25_day = 'NULL'

                data = '(\'{}\',\'{}\',{},{},{},{},{},{},{},{})'.format(
                    ticker_symbol,          # security symbol
                    format_date(row[0]),    # date
                    Decimal(row[1]),        # open
                    Decimal(row[2]),        # high
                    Decimal(row[3]),        # low
                    Decimal(row[4]),        # close
                    int(row[5]),            # volume
                    Decimal(row[6]),        # adj_close
                    mva_10_day,             # 10 day mva
                    mva_25_day              # 25 day mva
                )
                counter += 1

    except urllib2.URLError as e:
        print e

    print counter, ' rows added'


if __name__ == '__main__':
    if len(argv) != 2:
        print 'Proper Usage:\n\tpython loader_finance.py <ticker name>'
        exit(1)
    ticker_name = str(argv[1]).upper()
