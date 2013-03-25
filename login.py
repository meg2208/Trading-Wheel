
from credentials import username,password,server
from os import system as sys

sys( "sqlplus {}/{}@{}".format(username,password,server) )

