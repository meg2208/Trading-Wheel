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

class Login_Form(Form):
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
            raise StopValidation("Wrong username")

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
        

