import aggregate_portfolio as portfolio
import os, sys
import trade
import datetime
# sys.path.append() #move to root
from credentials import username,password,server
import cx_Oracle as oracle

class controller():

    portfolios = []
    all_cash = True
    db = oracle.connect("{}/{}@{}".format(username,password,server))
    cursor = db.cursor()

    def __init__(self):
        self.portfolios = []
        self.all_cash = True


    def connect(self):
        db = oracle.connect("{}/{}@{}".format(username,password,server))
        cursor = db.cursor()
        return db,cursor


    def import_ports(self, sid):        
 #       db = oracle.connect("{}/{}@{}".format(username,password,server))
  #      cursor = db.cursor()
        db, cursor = connect()
        strat_id = sid
        cursor.execute("""
            SELECT ag.* 
                FROM aggregate_portfolio ag, day_to_day dtd
                WHERE dtd.portfolio_id = ag.portfolio_id
                AND dtd.strategy_id = """+strat_id+"""
                ORDER BY ag.time""" 
              )
        ports = cursor.fetchall()
        return ports
       


if __name__ == '__main__'(self):
    db, cursor = connect()
    ports = import_ports('1000')
    #   portfolios = [portfolio.aggregate_portfolio(x[0],x[1],x[2],x[3],x[4],x[5],x[6]) for x in ports]
    i = 0
    print 'hi'
    for x in ports:
        portfolios.append(portfolio.aggregate_portfolio(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
    cursor.close()
    db = oracle.connect("{}/{}@{}".format(username,password,server))
    cursor = db.cursor()
    #   db, cursor = connect()
    for i in portfolios:
        i.import_trades()
    a = 0
    print 'got here...'
    for z in portfolios:
        z.free_cash = (1+(z.interest_rate/365)) * portfolios[a-1].free_cash
        z.portfolio_value = z.free_cash + z.securities_value
        if len(z.makes_trade):                
            z.full_update()
