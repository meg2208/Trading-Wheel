from math import ceil
from datetime import datetime


class Portfolio:
    "Day to day portfolio, also shows trades"

    def __init__(self, day, cash, stocks, trades, holdings=None):
        self.day = day
        self.cash = cash
        self.stock_value = 0
        self.holdings = holdings
        self.trades = trades
        for trade in self.trades:
            price = int(stocks[trade.ticker].days[day].close_price)
            if trade.buy:   # If buying
                cash_to_spend = self.cash * trade.allocation
                shares_bought = int(cash_to_spend/price)
                self.cash -= shares_bought * price
                if trade.ticker in holdings:
                    holdings[trade.ticker] += shares_bought
                else:
                    holdings[trade.ticker] = shares_bought
                trade.shares = shares_bought   # updating trade

            else:   # If selling
                if trade.ticker in holdings:
                    shares_sold = int(ceil(holdings[trade.ticker] *
                                      trade.allocation))
                    self.holdings[trade.ticker] -= shares_sold
                    self.cash += shares_sold * price
                    trade.shares = shares_sold

        self.trades = trades

        for security in holdings.keys():   # dictionary, ticker -> shares
            try:
                price = int(stocks[security].days[day].close_price)
                self.stock_value += holdings[security] * price
            except KeyError:
                print 'holiday, stock market closed on {}'.format(day)

        self.value = int(self.cash + self.stock_value)
        self.stock_value = int(self.stock_value)
        self.cash = int(self.cash)

    def __str__(self):
        return "day: {}\n\tvalue: {}\n\tcash: {}".format(
            self.day, int(self.value), int(self.cash))

    def graph_info(self):
        return """
        data.addColumn('date', 'Date');
        data.addColumn('number', 'Portfolio Value');
        data.addColumn('string', 'title1');
        data.addColumn('string', 'text1');
        data.addColumn('number', 'Cash');
        data.addColumn('number', 'Securities Value');
        """

    def graph_value(self):
        date = datetime.strptime(self.day, "%Y-%m-%d")
        return [date, self.value, None, None, self.cash, self.stock_value]
