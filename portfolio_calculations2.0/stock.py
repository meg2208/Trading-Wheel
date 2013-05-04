
from trade import Trade
from datetime import datetime, timedelta


class Stock:

    def __init__(self, tick, mva):
        self.ticker = str(tick)
        self.first_day = None
        self.mva = mva
        self.days = {}
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
        if under > over:
            longest_mva = under
        else:
            longest_mva = over

        first_pd = datetime.strptime(self.first_day, "%Y-%m-%d")
        first_pd = nth_weekday(first_pd, longest_mva)
        first_pd = "{}-{}-{}".format(first_pd.year, str(first_pd.month).zfill(2),
                                     str(first_pd.day).zfill(2))

        over_on_top = None      # initiating
        if self.days[first_pd].mva[under] < self.days[first_pd].mva[over]:
            over_on_top = True
        else:
            over_on_top = False

        day_keys = sorted(self.days.keys())
        for date in day_keys:
            day = self.days[date]
            if mva_flip_spots(day, under, over, over_on_top):
                over_on_top = not over_on_top
                if over_on_top:
                    trades.append(Trade(self.ticker, day.date, allocation,
                                        buy_sell))

        self.trade_sets.append(trades)


def mva_flip_spots(day, under, over, current_state):
    if day.mva[under] < day.mva[over] and not current_state:
        return True     # 'over' cross over 'under'
    if day.mva[under] > day.mva[over] and current_state:
        return True     # 'under' cross over 'over'
    return False


def nth_weekday(the_date, num_days):
    """ the_date : datetime object
        num_days : the number of weekdays you'd like to skip
        assumes that the_date is a weekday  """
    weeks = num_days / 5
    day = the_date.weekday() + (num_days % 5)
    if day > 4:
        day += 2
    num_days = weeks*7 + day - the_date.weekday()
    diff = timedelta(days=num_days)
    new_date = the_date + diff
    return new_date
