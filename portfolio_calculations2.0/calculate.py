from get_stocks import get_data


def calculate(triggers, starting_cash=100000):
    stocks = get_stocks(triggers)
    print stocks

    find_all_trades(starting_cash, stocks)


def get_stocks(triggers):
    """
    Returns the relevant stock data for all passed in trades.
    Finds all potential trades.
    """
    stocks = {}
    for trigger in triggers:
        if trigger.ticker in stocks:
            stocks[trigger.ticker] = stocks[trigger.ticker] | (trigger.mva_1,
                                                               trigger.mva_2)
        else:
            stocks[trigger.ticker] = set([trigger.mva_1, trigger.mva_2])

    "Getting all stock data and calculating MVAs"
    stock_data = []
    for stock in stocks.keys():
        stock_data.append(get_data(stock, stocks[stock]))

    "Finding potential trades/sells"
    for trigger in triggers:
        for i in range(len(stock_data)):
            if stock_data[i].ticker == trigger.ticker:
                break

        stock_data[i].find_trades(
            trigger.mva_1, trigger.mva_2, trigger.action, trigger.allocation,
            trigger.action_ticker)

    return stock_data


def find_all_trades(starting_cash, stocks):
    potential_trades = []
    for stock in stocks:
        for trades in stock.trade_sets:
            potential_trades += trades

    potential_trades.sort()

    for trade in potential_trades:
        print trade

    return potential_trades
