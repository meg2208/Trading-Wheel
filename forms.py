from wtforms import Form, BooleanField, TextField, PasswordField, \
    validators, ValidationError
import cx_Oracle as oracle
import credentials 

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
    username    = TextField('Username', [validators.Length(min=5,max=20)]) 
    password 	= PasswordField('New Password', [
    	validators.Required(),
    	validators.EqualTo('confirm', message='Passowrds must match')])
    confirm		= PasswordField('Confirm Password')
    accept_tos	= BooleanField('I accept the terms of service',[
    	validators.Required()])

    def validate_username(form,field):
        raise ValidationError('testing')

class Login_Form(Form):
    username    = TextField('Username' )


