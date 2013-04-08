
from wtforms import Form, BooleanField, TextField, PasswordField, \
    validators, ValidationError
import cx_Oracle as oracle
from scripts import credentials

# Connecting to oracle database
def connect():
    db = oracle.connect("{}/{}@{}".format(credentials.username,
        credentials.password, credentials.server))
    cursor = db.cursor()
    return db,cursor

#Closing connections
def close(db,cursor):
    cursor.close()
    db.close()


"""
Register User Form
"""
class Register_Form(Form):
    username    = TextField( 'Username' ) 
    password 	= PasswordField('New Password', [
    	validators.Required(),
    	validators.EqualTo('confirm', message='Passwords must match')])
    confirm		= PasswordField('Confirm Password')
    accept_tos	= BooleanField('I accept the terms of service',[
    	validators.Required()])

    def validate_username(form,field):
        if len(field.data) > 20 or len(field.data) < 4:
            raise ValidationError('Username must between 5 and 20 '+
                'characters')
        sql_query = """
        SELECT *
        FROM 
            user_data
        WHERE 
            user_id = '{}'""".format( field.data )
        db,cursor = connect()
        data = cursor.execute( sql_query ).fetchall()
        close(db,cursor)
        if len( data ) == 1:
            raise ValidationError('Username already in use')


"""
Log in user form
"""
class Log_in_Form(Form):
    username    = TextField('Username' )
    password    = PasswordField('Password' )

    def validate_username(form,field):
        sql_query = """
        SELECT user_id
        FROM 
            user_data
        WHERE 
            user_id = '{}' """.format( field.data )
        db,cursor = connect()
        data = cursor.execute( sql_query ).fetchall()
        close(db,cursor)
        if len( data ) != 1:
            raise ValidationError("Wrong username")

    def validate_password(form,field):
        sql_query = """
        SELECT password
        FROM 
            user_data
        WHERE 
            user_id = '{}' """.format( form.username.data )
        db,cursor = connect()
        data = cursor.execute( sql_query ).fetchall()
        close(db,cursor)
        if data[0][0] != field.data:
            raise ValidationError('Wrong password')


"""
Create Strategy form
"""
class Create_Strategy_Form(Form):
    strat_name  = TextField('Strategy Name', [
        validators.Required(),
        validators.Length(min=10,max=200)])

"""
Create Indicator form
"""
class Create_Indicator_Form(Form):
    security    = TextField('Ticker Name', [
        validators.Required(),
        validators.Length(min=1,max=6)])
    mva_10      = BooleanField('10 day moving average')
    mva_25      = BooleanField('25 day moving average')

    def validate_mva_10(form,field):
        if form.mva_25.data == True and field.data == True:
            raise ValidationError('You can only choose one reference')
        if form.mva_25.data == False and field.data == False:
            raise ValidationError('You must choose at least one reference')

#    def get_strategies(username):
#        sql_query ="""
#        SELECT S.strategy
#        FROM user_data U, create_strategy CS, strategy S,
#        WHERE user_id = {} AND
#            user_data.user_id = CS.user_id AND
#            CS.strategy_id = S.strategy_id
#        """.format( username )
#        db,cursor = connect()
#        cursor.execute(sql_query)
#        data = cursor.fetchall()[0][0]









