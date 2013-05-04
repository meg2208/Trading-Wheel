from get_stocks import get_data
from portfolio import Portfolio
from datetime import datetime, timedelta


def calculate(triggers, starting_cash=100000):
    stocks = get_stocks(triggers)
    print stocks

    trades = find_all_trades(starting_cash, stocks)

    portfolios = fill_out_trades(starting_cash, trades, stocks)

    trades = []
    for day in portfolios:
        trades = trades + day.trades

    for trade in trades:
        if trade.shares:
            print trade

    for day in portfolios:
        print day.day, day.value


def get_stocks(triggers):
    """
    Returns the relevant stock data for all passed in trades.
    Finds all potential trades.
    """
    stocks = {}     # ticker -> set( all MVA's )
    for trigger in triggers:
        if trigger.ticker in stocks:
            stocks[trigger.ticker] = stocks[trigger.ticker] | set(
                [trigger.mva_1, trigger.mva_2])
        else:
            stocks[trigger.ticker] = set([trigger.mva_1, trigger.mva_2])

    "Getting all stock data and calculating MVAs"
    stock_data = {}     # ticker -> Stock object
    for stock in stocks.keys():
        stock_data[stock] = get_data(stock, stocks[stock])

    "Finding potential trades/sells"
    for trigger in triggers:
        stock_data[trigger.ticker].find_trades(
            trigger.mva_1, trigger.mva_2, trigger.action, trigger.allocation,
            trigger.action_ticker)

    return stock_data


def find_all_trades(starting_cash, stocks):
    potential_trades = []
    for stock_key in stocks.keys():
        security = stocks[stock_key]
        for trades in security.trade_sets:
            potential_trades += trades

    return sorted(potential_trades)


def fill_out_trades(starting_cash, trades, stocks):
    """ starting_cash : int
        trades : date_str -> trade object
        stocks : ticker -> stock object
    """
    oldest_stock = stocks[sorted(stocks.keys())[0]]
    earliest_day = oldest_stock.first_day

    for stock_key in stocks.keys():
        stock = stocks[stock_key]
        if stock.first_day < earliest_day:
            oldest_stock = stock
            earliest_day = stock.earliest_day
    date = datetime.strptime(earliest_day, "%Y-%m-%d")
    now = datetime.now()

    portfolios = []
    cash = starting_cash
    holdings = {}
    trade_dex = 0
    num_trades = len(trades)

    while date < now:
        day = "{}-{}-{}".format(date.year, str(date.month).zfill(2),
                                str(date.day).zfill(2))
        trades_list = []
        while trade_dex is not num_trades and trades[trade_dex].date == day:
            trades_list.append(trades[trade_dex])
            trade_dex += 1

        new_port = Portfolio(day, cash, stocks, trades_list, holdings)
        cash = new_port.cash
        holdings = new_port.holdings
        portfolios.append(new_port)
        date += timedelta(days=1)

        next_day = True
        while next_day and date < now:
            try:
                day = "{}-{}-{}".format(date.year, str(date.month).zfill(2),
                                        str(date.day).zfill(2))
                oldest_stock.days[day]
                next_day = False
            except KeyError:
                date += timedelta(days=1)

    return portfolios
