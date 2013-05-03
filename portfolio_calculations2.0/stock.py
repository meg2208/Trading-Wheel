
from trade import Trade


class Stock:

    def __init__(self, tick, mva):
        self.ticker = str(tick)
        self.mva = mva
        self.days = []
        self.trade_sets = []

    def __str__(self):
        return "ticker {}\nnum days: {}".format(
            self.ticker, len(self.days))

    """
    Finds all instances of where the 'over' MVA cross over the other option
    """
    def find_trades(self, under, over, buy_sell, allocation,
                    action_ticker=None):
        if not action_ticker:
            action_ticker = self.ticker
        trades = []

        over_on_top = None      # initiating
        first = self.days[0]
        if first.mva[under] < first.mva[over]:
            over_on_top = True
        else:
            over_on_top = False

        for day in self.days:
            if mva_flip_spots(day, under, over, over_on_top):
                over_on_top = not over_on_top
                if over_on_top:
                    print 'Trade made!'
                    trades.append(Trade(self.ticker, day.date, allocation,
                                        buy_sell))

        self.trade_sets.append(trades)


def mva_flip_spots(day, under, over, current_state):
    if day.mva[under] < day.mva[over] and not current_state:
        return True     # 'over' cross over 'under'
    if day.mva[under] > day.mva[over] and current_state:
        return True     # 'under' cross over 'over'
    return False
