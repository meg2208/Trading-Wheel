import datetime
import os, sys
sys.path.append("/Users/mgarbis/github/Trading-Wheel/scripts")
from credentials import username,password,server
import cx_Oracle as oracle

class trade():

    	portfolio_id = 0 #from makes_trade
    	trade_id = 0 ##
    	security = ""
    	action = 0
    	share_amount = 0
    	price = 0
    	time = datetime.date

        #sets the values equal to the original trigger
    	def __init__(self, pid, tid, s, a, sh, pr, t):
                self.portfolio_id = pid
                self.trade_id = tid
                self.security = s
                self.action = a
                self.share_amount = sh
                self.price = pr
                self.time = t

    