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
    populate_mva(strategy_id)
    pop_skeleton(strategy_id)
    pop_trades(strategy_id)
    set_start_vals(strategy_id)


# reference is volume or adj_price
# dbcolname is MVA_10_DAY or MVA_25_DAY
# period is amount of days
# run this before running backtest_prep
# then you are ready to run the backtest
def populate_mva(strategy_id):
    db, cursor = connect()
    with file('../queries/mva.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
    cursor.execute(sql_update)
    db.commit()
    close(db, cursor)


def set_rdp_relation(strategy_id):
    db, cursor = connect()
    B = 'B'
    S = 'S'
    with file('../queries/set_rdp_relationB.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
        cursor.execute(sql_update)
        db.commit()
    with file('../queries/set_rdp_relationS.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
        cursor.execute(sql_update)
        db.commit()
        close(db, cursor)


def pop_skeleton(strategy_id):
    db, cursor = connect()
    with file('../queries/initial_agg_port_and_dtd.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
    cursor.execute(sql_update)
    db.commit()
    close(db, cursor)


def pop_trades(strategy_id):
    db, cursor = connect()
    with file('../queries/pop_temp_b_x_over.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
    cursor.execute(sql_update)
    db.commit()
    with file('../queries/pop_temp_s_x_under.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
    cursor.execute(sql_update)
    db.commit()
    close(db, cursor)


def set_start_vals(strategy_id):
    db, cursor = connect()
    with file('../queries/set_portfolio_start_values.sql', 'r') as update:
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
    a = 0
    print 'got here...'
    for z in portfolios:
        if a == 0:
            ''
        else:
            z.daily_update(portfolios[a-1].get_cash_amt())
        print 'portfolio value ', z.portfolio_value
        if len(z.makes_trade):
            z.full_update()
        a += 1
