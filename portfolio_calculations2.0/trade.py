

class Trade:

    def __init__(self, ticker, date, goal, buy, shares=None):
        self.ticker = ticker
        self.date = date
        self.shares = shares
        self.buy = buy
        self.attempt = None             # Shares attempted to buy
        if goal:                        # allocation intended to use
            self.goal = float(goal)
        else:
            self.goal = goal

    def get_data(self):
        if self.buy:
            decision = 'Bought'
        else:
            decision = 'Sold'
        return [self.date,
                self.ticker,
                self.shares,
                decision]

    def __str__(self):
        if self.buy:
            decision = 'Buy'
        else:
            decision = 'Sell'

        return "{}\n\t{} {}".format(
            self.date, decision, self.goal, self.ticker)

    def __cmp__(self, other):
        if self.date == other.date:
            return 0
        elif self.date < other.date:
            return -1
        elif self.date > other.date:
            return 1
