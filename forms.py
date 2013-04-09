
import cx_Oracle as oracle
from scripts import credentials
from wtforms import Form, BooleanField, TextField, PasswordField, \
    validators, ValidationError, SelectField


# Connecting to oracle database
def connect_db():
    db = oracle.connect("{}/{}@{}".format(credentials.username,
                                          credentials.password,
                                          credentials.server))
    cursor = db.cursor()
    return db, cursor


#Closing connections
def close_db(db, cursor):
    cursor.close()
    db.close()


##################################
#Register User Form
##################################
class Register_Form(Form):
    username = TextField('Username')
    Password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    accept_tos = BooleanField('I accept the terms of service', [
                              validators.Required()])

    def validate_username(form, field):
        if len(field.data) > 20 or len(field.data) < 4:
            raise ValidationError('Username must between 5 and 20 ' +
                                  'characters')
        sql_query = """
        SELECT *
        FROM
            user_data
        WHERE
            user_id = '{}'""".format(field.data)
        db, cursor = connect_db()
        data = cursor.execute(sql_query).fetchall()
        close_db(db, cursor)
        if len(data) is 1:
            raise ValidationError('Username already in use')


####################################
# Log In Form
#####################################
class Log_in_Form(Form):
    username = TextField('Username')
    password = PasswordField('Password')

    def validate_username(form, field):
        sql_query = """
        SELECT user_id
        FROM
            user_data
        WHERE
            user_id = '{}' """.format(field.data)
        db, cursor = connect_db()
        data = cursor.execute(sql_query).fetchall()
        close_db(db, cursor)
        if len(data) != 1:
            raise ValidationError("Wrong username")

    def validate_password(form, field):
        sql_query = """
        SELECT password
        FROM
            user_data
        WHERE
            user_id = '{}' """.format(form.username.data)
        db, cursor = connect_db()
        data = cursor.execute(sql_query).fetchall()
        close_db(db, cursor)
        if data[0][0] != field.data:
            raise ValidationError('Wrong password')


##########################################
# Create Strategy form
###########################################
class Create_Strategy_Form(Form):
    strat_name = TextField('Strategy Name', [
        validators.Required(),
        validators.Length(min=10, max=200)])





#    def get_strategies(username):
#        sql_query ="""
#        SELECT S.strategy
#        FROM user_data U, create_strategy CS, strategy S,
#        WHERE user_id = {} AND
#            user_data.user_id = CS.user_id AND
#            CS.strategy_id = S.strategy_id
#        """.format( username )
#        db,cursor = connect_db()
#        cursor.execute(sql_query)
#        data = cursor.fetchall()[0][0]
