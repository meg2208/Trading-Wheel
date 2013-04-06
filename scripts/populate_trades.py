import cx_Oracle as oracle
from credentials import username,password,server

#####
# Populates trade info [not completed]
####

def connect():
    db = oracle.connect("{}/{}@{}".format(username,password,server))
    cursor = db.cursor()
    return db,cursor

def close(db,cursor):
    cursor.close()
    db.close()

def populate reference(start_time,end_time,L_indicator_id,
	R_indicator_id,buy_sell,operator,action_security,
	share_amount,allocation,cash_value)
	
	with file('queries/insert_ind_ref.sql','r') as update:
		sql_update = update.read().format(start_time,
			end_time,L_indicator_id, R_indicator_id,
			buy_sell,operator,action_security,
			share_amount,allocation,cash_value)
		cursor.execute( sql_update )
		db.commit()

#first have to decide when a buy or sell is signaled
def trigger_signals(strategy_id) 
	