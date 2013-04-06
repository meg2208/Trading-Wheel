from wtforms import Form, BooleanField, TextField, PasswordField, validators

class Register_Form(Form):
    username    = TextField('Username', [validators.Length(min=5,max=20)]) 
    password 	= PasswordField('New Password', [
    	validators.Required(),
    	validators.EqualTo('confirm', message='Passowrds must match')])
    confirm		= PasswordField('Confirm Password')
    accept_tos	= BooleanField('I accept the terms of service',[
    	validators.Required()])


