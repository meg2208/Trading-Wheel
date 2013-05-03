

class Trigger:

    def __init__(self, ticker, mva_range_1, mva_range_2, action,
                 action_ticker, allocation):
        self.ticker = ticker
        self.mva_1 = mva_range_1
        self.mva_2 = mva_range_2
        self.action = action
        self.action_ticker = action_ticker
        self.allocation = allocation
