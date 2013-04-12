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

    def __init__(self, pid, t, pv, ir, sv, fc, pvc):
        self.portfolio_id = pid
        self.time = t
        self.portfolio_value = pv
        self.interest_rate = ir
        self.securities_value = sv
        self.free_cash = fc
        self.portfolio_value_change = pvc
 #       if self.free_cash != 0:
  #          self.all_cash = False
   #     else:
    #        self.all_cash = True
        self.makes_trade = []
        self.portfolio_contents = []

    def get_all_values(self):
        x = self.portfolio_contents, self.free_cash 
      #  self.securities_value, self.portfolio_value
        return x

    def get_cash_amt(self):
        return self.free_cash

    def daily_update(self, x):
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
            self.makes_trade = [trade(self.portfolio_id, x[0], x[1], x[2],
                                x[3], x[4], x[5], x[6]) for x in trades]

    def get_price(self, sec):
        db, cursor = connect()
        cursor.execute("""
            SELECT q.adj_close
                FROM query_data q
                WHERE q.security = (:sec) AND
                q.time = (:mydate)""", {'mydate': self.time,
                                        'sec': str(sec)})
        price = cursor.fetchall()
        close(db, cursor)
        print price
        return price[0][0]

    def calc_amts(self, sec, amt, allo, val, action):
        if action == 'B':
            return self.buy_calc_amts(sec, amt, allo, val)
        else:
            return self.sell_calc_amts(sec, amt, allo, val)

    def buy_calc_amts(self, sec, amt, allo, val):
        print 'buy... '
        print 'price of ' + sec + 'is ', self.get_price(sec)
        print 'currently have ', self.get_current_amt(sec), 'of ', sec
        print 'portfolio value is ', self.portfolio_value
        price = self.get_price(sec)
        current = self.get_current_amt(sec)
        shares = 0
        allocation = 0
        #amount = 0
        #value = 0

        if amt > 0:
            if current == 0 and amt*price < self.free_cash:
                shares = amt
            elif current < amt and (amt - current)*price < self.free_cash:
                shares = amt - current
        #    amount = shares
        elif allo > 0:
            if allo*self.portfolio_value < self.free_cash and current == 0:
                shares = int((allo*self.portfolio_value)/price)
            elif current != 0 and (allo*self.portfolio_value - price*current) < self.free_cash:
                shares = int((allo*self.portfolio_value - price*current)/price)
            else:
                shares = int(self.free_cash/price)
            print "shares are ", shares
            print "price is ", price
            suggested_amt = operator.mul(shares,int(price))
            allocation = suggested_amt/self.portfolio_value
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
        if self.get_current_amt(sec) is None:
            current = 0
        else:
            current = self.get_current_amt(sec)
        price = float(self.get_price(sec))
        shares = 0
        amount = 0
        allocation = 0
        value = 0

        print 'alloc', type(alloc)
        print 'current', type(current)
        print 'price', type(price)

        if current == 0:
            ''
        elif amt > 0:
            # if you have more than you are supposed to sell, sell all
            if current < amt:
                shares = current
            elif current > amt:
                shares = amt
            amount = shares
        elif alloc > 0:
            tot_current = current*price
            suggested_alloc = alloc
            total_suggested_amt = tot_current*suggested_alloc
            shares_a = total_suggested_amt/price
            shares = int(shares_a)
        #    amount = (shares*price)/self.portfolio_value
        # elif val > 0:
        #     if val < current*price:
        #         shares = int(val/price)
        #     else:
        #         shares = current
        #     value = shares*price
        return -1*shares, allocation, price

    def get_current_amt(self, sec):
        amount = 0
        if len(self.portfolio_contents) > 0:
            for secs in self.portfolio_contents:
                if secs.security == sec:
                    amount = secs.share_amount
                    return amount
        else:
            return amount

    def add_contents(self, sec, shares):
        self.portfolio_contents.append(security_state(self.portfolio_id, sec, shares))

    def update_securities(self, sec, shares, price):
        if len(self.portfolio_contents) > 0:
            for securities in self.portfolio_contents:
                if securities.security == sec:
                    securities.share_amount += shares
        else:
            self.add_contents(sec, shares)

        #portfolio value doesnt change when a security is purchased/sold
        self.securities_value += shares*price
        self.free_cash -= shares*price


    def full_update(self):
        if len(self.makes_trade) > 0:
            print 'trade happened'
            for trades in self.makes_trade:
       #         security = trades.security
                shares, allocation, price = self.calc_amts(trades.security, trades.share_amount,
                                                    trades.allocation, 0, trades.action)
                trades.share_amount = shares
                trades.allocation = allocation
                self.update_securities(trades.security, shares, price)
        self.update_in_db()

    def update_in_db(self):
        db, cursor = connect()
        self.push_ag_to_db(cursor, db)
        

    def push_ag_to_db(self, cursor, db):
        sql_update = """
        UPDATE aggregate_portfolio ag
        SET
            ag.portfolio_value = {0},
            ag.securites_value = {1},
            ag.free_cash = {2}
        WHERE 
            ag.portfolio_id = {3}""".format(self.portfolio_value,
                        self.securities_value, self.free_cash, self.portfolio_id)
        cursor.execute(sql_update)
        db.commit()
        close(db, cursor)


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
        #self.update_securities()
        #self.update_portfolio_value()


class security_state():

    portfolio_id = 0
    security = ''
    share_amount = 0
    changed = True

    def __init__(self, pid, sec, sh):
        self.portfolio_id = pid
        self.security = sec
        self.share_amount = sh
        self.changed = True