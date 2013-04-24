import datetime
import operator
# sys.path.append() #move to root
from credentials import username, password, server
import cx_Oracle as oracle


def connect():
    db = oracle.connect("{}/{}@{}".format(username,
                        password, server))
    cursor = db.cursor()
    return db, cursor

def close(db, cursor):
    cursor.close()
    db.close()


class aggregate_portfolio():

    all_cash = True
    portfolio_id = 0
    time = datetime.date
    portfolio_value = 0
    interest_rate = 0
    securities_value = 0
    free_cash = 0
    portfolio_value_change = 0
    portfolio_contents = []  # contains all security_state objects for the given day
    makes_trade = []  # contains all trade objects for the given day
    stock_prices = {}


    def __init__(self, pid, t, pv, ir, sv, fc, pvc):
        self.portfolio_id = pid
        self.time = t
        self.portfolio_value = pv
        self.interest_rate = ir
        self.securities_value = sv
        self.free_cash = fc
        self.portfolio_value_change = pvc
        self.makes_trade = []
        self.portfolio_contents = []

    # returns all values of the stock
    def get_all_values(self):
        x = self.portfolio_contents, self.free_cash
        return x

    #  
    def get_cash_amt(self):
        return self.free_cash


    def daily_update(self, x, stock_prices):
        print 'today is ', self.time
        self.stock_prices = stock_prices
        yest_contents = x[0]
        yest_cash = x[1]
        self.portfolio_contents = yest_contents
        self.free_cash = (1+(self.interest_rate/365)) * yest_cash
        self.securities_value = self.current_securities_value()
        self.portfolio_value = self.securities_value + yest_cash


    def current_securities_value(self):
        value = 0
        if len(self.portfolio_contents) > 0:
            for securities in self.portfolio_contents:
                value += self.get_price(securities.security)*securities.share_amount
                print 'you have ', securities.share_amount, ' shares of ', securities.security
        return value

    def import_trades(self, db):
        cursor = db.cursor()
        cursor.execute("""
            SELECT t.*
                FROM makes_trade mt,
                 trade t
                WHERE t.trade_id = mt.trade_id AND
                mt.portfolio_id = {} """.format(str(self.portfolio_id)))
        trades = cursor.fetchall()
        print 'portfolio_value is ', self.portfolio_value
        if trades:
            print 'TRADETRADETRADETRADETRADETRADE'
            print self.time
            for x in trades:
                self.makes_trade.append(trade(self.portfolio_id, x[0], x[1], x[2],
                                x[3], x[4], x[5], x[6]) )

    def get_price(self, sec):
        date = self.time
        price = self.stock_prices[(sec, date)][5]
        return price

    def calc_amts(self, sec, amt, allo, val, action):
        if action == 'B':
            return self.buy_calc_amts(sec, amt, allo, val)
        else:
            return self.sell_calc_amts(sec, amt, allo, val)

    def buy_calc_amts(self, sec, amt, allo, val):
        print 'buy... '
        print 'price of ' + sec + 'is ', self.get_price(sec)
        print 'currently have ', self.get_current_amt(sec), ' share of ', sec
        print 'portfolio value is ', self.portfolio_value
        print 'DESIRED ALLOCATION IS ', allo
        price = self.get_price(sec)
        current = self.get_current_amt(sec)
        current_amt = current*price
        shares = 0
        allocation = 0
        #amount = 0
        #value = 0


        if allo > 0.0:
            print 'GOT HERE YOU STUPID BITCH'
            amt_desired = operator.mul(allo,self.portfolio_value)

            # have enough and don't have the stock --> buy all desired
            if amt_desired < float(self.free_cash) and current == 0:
                shares = int(amt_desired/price)

            # have enough and do have the stock --> buy remaining amount to reach desired allocation
            elif current != 0 and (amt_desired - current_amt) < float(self.free_cash):
                shares = int((amt_desired - current_amt)/price)
           
            # don't have enough and don't have the stock --> use all remaining cash
            elif amt_desired > self.free_cash and current == 0:
                shares = int(self.free_cash/price)

            # don't have enough and have the stock --> use all remaining cash
            elif current != 0 and (amt_desired - current_amt) > float(self.free_cash):
                shares = int(self.free_cash/price)

            #not 100% sure if this  will ever be triggered
            else:
                return 0, 0, price

            print "time to buy ", shares
            print "buying them for ", price
            amt_to_purchase = operator.mul(shares,int(price))
            allocation = amt_to_purchase/float(self.portfolio_value)
            print "allocation is ", allocation

        elif amt > 0.0:
            if current == 0 and amt*price < self.free_cash:
                shares = amt
            elif current < amt and (amt - current)*price < self.free_cash:
                shares = amt - current
        # elif val > 0:
        #     if val < self.free_cash and current == 0:
        #         shares = int(val/price)
        #     elif val > self.free_cash and current != 0:
        #         shares = int(self.free_cash/price)
        #     value = shares*price
        return shares, allocation, price



    # allo refers to an allocation of your current amount of
    # that security that you have
    # that you would like to remove
    def sell_calc_amts(self, sec, amt, alloc, val):
        print 'sell... '
        print 'price of ' + sec + 'is ', self.get_price(sec)
        print 'currently have ', self.get_current_amt(sec), 'of ', sec
        print 'portfolio value is ', self.portfolio_value
        
        price = float(self.get_price(sec))
        current = self.get_current_amt(sec)
        current_amt = current*price

        shares = 0
#        amount = 0
        allocation = 0
        value = 0

        print 'alloc', type(alloc)
        print 'current', type(current)
        print 'price', type(price)

        # can't sell something you don't have (no margin support yet)
        if current == 0:
            return 0, 0, price

        # amt is the amount of shares you originally wanted to sell
        elif amt > 0.0:

            # if you have less than you are supposed to sell --> sell all
            if current < amt:
                shares = current

            # if you have more than you are supposed to sell --> sell desired amount
            elif current > amt:
                shares = amt

        # the allocation to sell here represents the percentage of your 
        #  current position in the stock
        elif alloc > 0.0:
            allocation = alloc
            total_suggested_amt = current_amt*allocation
            shares_a = total_suggested_amt/price
            shares = int(shares_a)
        #    amount = (shares*price)/self.portfolio_value
        # elif val > 0:
        #     if val < current*price:
        #         shares = int(val/price)
        #     else:
        #         shares = current
        #     value = shares*price
        return -1*shares, -1*allocation, price



    # returns amount of shares held by a given security at the current time
    def get_current_amt(self, sec):
        amount = 0
        if len(self.portfolio_contents) > 0:
            for secs in self.portfolio_contents:
                if secs.security == sec:
                    amount = secs.share_amount
        return amount



    # called by update_securities
    def add_contents(self, sec, shares):
        self.portfolio_contents.append(security_state(self.portfolio_id, sec, shares))



    # the last step of the full update
    # goes through each security so shares reflect the day's trades
    def update_securities(self, sec, shares, price):
        print 'got here '
        found = False
        if len(self.portfolio_contents) > 0:
            for securities in self.portfolio_contents:
                if securities.security == sec:
                    found = True
                    securities.share_amount += shares
                    print 'increasing shares of ', sec, ' to ', securities.share_amount
        if found == False:
            print 'adding ', sec, ' to the portfolio'
            self.add_contents(sec, shares)

        #portfolio value doesnt change when a security is purchased/sold
        self.securities_value += shares*price
        self.free_cash -= shares*price


    # master method for updating when trades are made
    def full_update(self):
        if len(self.makes_trade) > 0:
            print 'trade happened'
            for trades in self.makes_trade:
                shares, allocation, price = self.calc_amts(trades.security, trades.share_amount,
                                                    trades.allocation, 0, trades.action)
                trades.share_amount = shares
                trades.allocation = allocation
                self.update_securities(trades.security, shares, price)

    # calls individual pushes for each entity set
    def update_in_db(self, db, cursor):
        db, cursor = self.push_ag_to_db(cursor, db)
        db, cursor = self.push_trades_to_db(cursor, db)
    #    db, cursor = self.push_contents_to_db(cursor, db)
        return db, cursor

    # updates aggregate portfolios in the db
    def push_ag_to_db(self, cursor, db):
        sql_update = """
        UPDATE aggregate_portfolio ag
        SET
            ag.portfolio_value = ROUND({0}, 2),
            ag.securites_value = ROUND({1}, 2),
            ag.free_cash = ROUND({2}, 2)
        WHERE 
            ag.portfolio_id = {3}""".format(self.portfolio_value,
                        self.securities_value, self.free_cash, self.portfolio_id)
        cursor.execute(sql_update)
        db.commit()
        return db, cursor

    # updates trades in the oracle db
    def push_trades_to_db(self, cursor, db):
        i = 0
        if len(self.makes_trade) > 0:
            print 'push_trades_to_db '
            print 'trades ' 
            for trades in self.makes_trade:
                print trades.share_amount, 'shares of ', trades.security
                sql_update = """
                UPDATE trade t
                SET
                    t.share_amount = ROUND({0}, 2),
                    t.allocation = ROUND({2}, 2)
                WHERE 
                    t.trade_id = {1}""".format(self.makes_trade[i].share_amount,
                        self.makes_trade[i].trade_id, self.makes_trade[i].allocation)
                cursor.execute(sql_update)
                db.commit()
                i = i+1
        return db, cursor

    def push_contents_to_db(self, cursor, db):
        if len(self.portfolio_contents) > 0:
            print 'push secs to db '
            for holdings in self.portfolio_contents:
                sql_insert = """
                INSERT ALL
                INTO SECURITY_STATE (state_id, security, security_price, share_amount)
                    VALUES(seq_stateid.nextval, {0}, {1}, {2})
                INTO PORTFOLIO_CONTENTS (trade_id, portfolio_id)
                    VALUES(seq_stateid.currval, {0}, {3})
                    """.format(self.portfolio_id, self.get_price(holdings.security), holdings.share_amount, holdings.security)
                cursor.execute(sql_insert)
                db.commit()
        return db, cursor

class trade():

    portfolio_id = 0  # from makes_trade
    trade_id = 0
    security = ""
    action = ""
    share_amount = 0
    allocation = 0
    price = 0
    time = datetime.date

    #sets the values equal to the original trigger
    def __init__(self, pid, tid, s, a, sh, al, pr, t):
        self.portfolio_id = pid
        self.trade_id = tid
        self.security = s
        self.action = a
        self.share_amount = sh
        self.allocation = al  # fix this later
        self.price = pr
        self.time = t


class security_state():

    portfolio_id = 0
    security = ''
    share_amount = 0

    def __init__(self, pid, sec, sh):
        self.portfolio_id = pid
        self.security = sec
        self.share_amount = sh