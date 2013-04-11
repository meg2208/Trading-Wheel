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


# make object
# call populate_mva
# call prepare_backtest
# call backtest

# period must be equal to "10_day" or "25_day"
def back_test(strat_id, reference, period):
    if period is '10_day':
        column_name = 'MVA_10_DAY'
    else:
        column_name = 'MVA_25_DAY'

    portfolios = []
    all_cash = True

    populate_mva()


# reference is volume or adj_price
# dbcolname is MVA_10_DAY or MVA_25_DAY
# period is amount of days
# run this before running backtest_prep
# then you are ready to run the backtest
def populate_mva(security, reference, period):
    if period is '10_day':
        column_name = 'MVA_10_DAY'
    else:
        column_name = 'MVA_25_DAY'

    db, cursor = connect()
    with file('../queries/mva_mod.sql', 'r') as update:
        sql_update = update.read().format("'"+str(security)+"'", reference, column_name, period)
    cursor.execute(sql_update)
    close(db, cursor)


def set_rdp_relation(strategy_id):
    db, cursor = connect()
    with file('../queries/set_rdp_relation.sql', 'r') as update:
        sql_update = update.read().format(strategy_id, 'B')
    cursor.execute(sql_update)
    with file('../queries/set_rdp_relation.sql', 'r') as update:
        sql_update = update.read().format(strategy_id, 'S')
    cursor.execute(sql_update)
    close(db, cursor)


def pop_skeleton(strategy_id):
    db, cursor = connect()
    with file('../queries/initial_agg_port_and_dtd.sql', 'r') as update:
        sql_update = update.read().format(strategy_id)
    cursor.execute(sql_update)
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
    close(db, cursor)


def backtest_prep(strategy_id):
    set_rdp_relation(strategy_id)
    pop_skeleton(strategy_id)
    pop_trades(strategy_id)
    set_start_vals(strategy_id)


def import_ports(sid):
#       db = oracle.connect("{}/{}@{}".format(username,password,server))
#      cursor = db.cursor()
    db, cursor = connect()
    strat_id = sid
    cursor.execute("""
        SELECT ag.*
            FROM aggregate_portfolio ag, day_to_day dtd
            WHERE dtd.portfolio_id = ag.portfolio_id
            AND dtd.strategy_id = """+strat_id+"""
            ORDER BY ag.time""")
    ports = cursor.fetchall()
    return ports


def backtest(portfolios):
    db, cursor = connect()
    ports = import_ports('1000')
    #   portfolios = [portfolio.aggregate_portfolio(x[0],x[1],x[2],x[3],x[4],x[5],x[6]) for x in ports]
    i = 0
    print 'hi'
    for x in ports:
        portfolios.append(portfolio.aggregate_portfolio(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
        print 'portfolio appended'
    cursor.close()
    db = oracle.connect("{}/{}@{}".format(username, password, server))
    cursor = db.cursor()
    #   db, cursor = connect()
    for i in portfolios:
        i.import_trades(db)
        print 'imported trades'
    a = 0
    print 'got here...'
    for z in portfolios:
        z.free_cash = (1+(z.interest_rate/365)) * portfolios[a-1].free_cash
        z.portfolio_value = z.free_cash + z.securities_value
        if len(z.makes_trade):
            z.full_update()
