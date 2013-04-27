import aggregate_portfolio as portfolio
from credentials import username, password, server
import cx_Oracle as oracle


def connect():
    db = oracle.connect("{}/{}@{}".format(username, password, server))
    cursor = db.cursor()
    return db, cursor


def close(db, cursor):
    cursor.close()
    db.close()

# to run the backtest, just run this with the strategy id
def backtest(strat_id):
    backtest_prep(strat_id)
    run_backtest(strat_id)

def backtest_prep(strategy_id):
    set_rdp_relation(strategy_id)
    print 'rdp done'
    populate_mva(strategy_id)
    print 'mva done'
    pop_skeleton(strategy_id)
    print 'skeleton done'
    pop_trades(strategy_id)
    print 'trades done'
    set_start_vals(strategy_id)
    print 'start vals done'


# reference is volume or adj_price
# dbcolname is MVA_10_DAY or MVA_25_DAY
# period is amount of days
# run this before running backtest_prep
# then you are ready to run the backtest
def populate_mva(strategy_id):
    db, cursor = connect()
    with file('queries/mva.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
    cursor.execute(sql_update)
    db.commit()
    close(db, cursor)


def set_rdp_relation(strategy_id):
    db, cursor = connect()
    with file('queries/set_rdp_relationB.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
        cursor.execute(sql_update)
        db.commit()
    with file('queries/set_rdp_relationS.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
        cursor.execute(sql_update)
        db.commit()
        close(db, cursor)


def pop_skeleton(strategy_id):
    db, cursor = connect()
    with file('queries/initial_agg_port_and_dtd.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
    cursor.execute(sql_update)
    db.commit()
    close(db, cursor)


def pop_trades(strategy_id):
    db, cursor = connect()
    with file('queries/pop_trades_L10_O_R25.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
        cursor.execute(sql_update)
        db.commit()
    with file('queries/pop_trades_L10_U_R25.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
        cursor.execute(sql_update)
        db.commit()
    with file('queries/pop_trades_L25_O_R10.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
        cursor.execute(sql_update)
        db.commit()
    with file('queries/pop_trades_L25_U_R10.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
        cursor.execute(sql_update)
        db.commit()
    close(db, cursor)


def set_start_vals(strategy_id):
    db, cursor = connect()
    with file('queries/set_portfolio_start_values.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
    cursor.execute(sql_update)
    db.commit()
    close(db, cursor)



def import_ports(sid):
    db, cursor = connect()
    strat_id = sid
    print strat_id
    cursor.execute("""
        SELECT
            ag.*
        FROM
            aggregate_portfolio ag, day_to_day dtd
        WHERE
            dtd.portfolio_id = ag.portfolio_id
            AND dtd.strategy_id = {}
        ORDER BY ag.time""".format(strat_id))
    ports = cursor.fetchall()
    close(db, cursor)
    return ports

# key (as a tuple) = ('AAPL', datetime.datetime(2013, 2, 28, 0, 0))
# results (as a tuple) = (open, high, low, close, volume, adj_close, mva_10_day, mva_25_day)
def get_stock_info(strategy_id):
    print 'starting'
    db, cursor = connect()
    print 'connected'
    sql_query = """SELECT qd.*
    FROM raw_data_parsing rdp, query_data qd 
    WHERE rdp.security = qd.security 
        AND rdp.time = qd.time
        AND rdp.security = qd.security
        AND rdp.strategy_id = {}""".format(strategy_id)
    print 'done query'
    cursor.execute(sql_query)
    stock_list = cursor.fetchall()
    print 'now making the list'
    stock_dict = dict([(element[:2], element[2:]) for element in stock_list])
    print 'done making the list'
    close(db, cursor)
    return stock_dict


def run_backtest(strategy_id):
    db, cursor = connect()
    ports = import_ports(strategy_id)
    portfolios = []
    i = 0
    for x in ports:
        portfolios.append(portfolio.aggregate_portfolio(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
        print 'time is ', portfolios[i].time
        print 'portfolio appended'
        i += 1
    for k in portfolios:
        print 'date of portfolio is ', k.time
        k.import_trades(db)
        print 'imported trades'

    #store stock prices in dictionary
    stock_info = get_stock_info(strategy_id)
    a = 0
    print 'got here...'
    for z in portfolios:
        if a == 0:
            ''
        else:
            z.daily_update(portfolios[a-1].get_all_values(), stock_info)
        if len(z.makes_trade) > 0:
            z.full_update()
        db, cursor = z.update_in_db(db, cursor)
        print z.portfolio_value
        a += 1
    close(db, cursor)