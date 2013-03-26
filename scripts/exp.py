
from credentials import username,password,server
from os import system as sys

# example from biliris
# exp userid=<userid>/<password>@ADB3 TABLES=table-1,table-2,...,table-n ROWS=Y

tables = [
'user_data',
'trade',
'strategy',
'query_data',
'portfolio_statistics',
'indicator',
'action',
'create_portfolio',
'create_strategy',
'criteria',
'indicator_reference',
'raw_data_parsing'
]
tables = ','.join(tables)

command = """
exp dump={}/{}@{} TABLES={} ROWS=Y
""".format(username,password,server,tables)

sys( command )






