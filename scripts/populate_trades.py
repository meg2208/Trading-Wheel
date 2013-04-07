import cx_Oracle as oracle
from credentials import username,password,server
import os
import sys

#####
# Populates trade info [not completed]
####

def hi():
    print 'hi'

def changeroot():
    os.chdir("/Users/mgarbis/github/Trading-Wheel")

def connect():
    db = oracle.connect("{}/{}@{}".format(username,password,server))
    cursor = db.cursor()
    return db,cursor

def close(db,cursor):
    cursor.close()
    db.close()


def populate_reference(start_time,end_time,L_indicator_id,
    R_indicator_id,buy_sell,operator,action_security,share_amount,allocation,cash_value):
    with file('queries/insert_ind_ref.sql','r') as update:
        sql_update = update.read().format(start_time,end_time,L_indicator_id, R_indicator_id,buy_sell, operator, action_security,share_amount, allocation, cash_value)
        cursor.execute( sql_update )
        db.commit()


def populate_indicator(indicator_id, security,mva_10_day, mva_25_day):
    changeroot()
    db, cursor = connect()
    with file('queries/insert_ind.sql','r') as update:
        sql_update = update.read().format(indicator_id, "'"+security+"'", "'"+mva_10_day+"'", "'"+mva_25_day+"'")
        print sql_update
        cursor.execute( sql_update )
        db.commit()


#first have to decide when a buy or sell is signaled
def trigger_signals(strategy_id):
    db, cursor = connect()
    with file('queries/triggers.sql','r') as update:
        sql_update = update.read().format(strategy_id)
        cursor.execute( sql_update )
        db.commit()

## if __name__ == '__main__':
