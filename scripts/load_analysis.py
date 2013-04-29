
import cx_Oracle as ora
from credentials import username, password, server

db = ora.connect("{}/{}@{}".format(username, password, server))
c = db.cursor()

## make the benchmark_contents_type
## sum of allocations == 1

print 'What is your strategy number?'
strat_id = int(raw_input())

i = 0
allocation_left = 1.0
choices = []

# Looping while getting choices
while True and i < 10:
    print "Enter in the benchmark ticker and it's allocation separated by a space."
    print "Enter nothing to end"
    print "You currently have {} left of your allocation".format(allocation_left)
 
    data = raw_input()
    if data == '':
        if len(choices) == 0: #redundancy
            choices.append((strat_id, 'SPY', 1.0))
        else:
            choices[-1][2] += allocation_left
        break

    ticker, allocation = data.split(' ')
    ticker = str(ticker)
    allocation = float(allocation)

    # make sure allocation is still left
    if allocation_left - allocation < 0.0:
        allocation = allocation_left
        allocation_left = 0.0
        i = 10  # breaks loops after appending
    else:
        allocation_left -= allocation

    choices.append((strat_id, ticker, allocation))
    i += 1

print 'CHOICES', choices

# Getting insert skelton 
with file() as f:
    sql_insert = f.read.format( choices )

c.execute(sql_insert)
print 'The insert has been executed!'

c.close()
db.close()

