

class Trigger:

    def __init__(self, ticker, mva_range_1, mva_range_2, action,
                 allocation, action_ticker=None):
        """ action == True means BUY
            action == False means SELL  """
        self.ticker = ticker
        self.mva_1 = mva_range_1
        self.mva_2 = mva_range_2
        self.action = action
        self.action_ticker = action_ticker
        if not action_ticker:               # B/S itself if not specified
            self.action_ticker = ticker
        self.allocation = allocation
