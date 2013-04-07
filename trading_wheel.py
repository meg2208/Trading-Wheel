
from flask import Flask, render_template, flash, \
	url_for, g, redirect, request
import forms
import cx_Oracle as oracle
from scripts import credentials,loader,load_finance

app = Flask(__name__)
app.config.from_object('flask_settings')

# Opens SQL*Plus db and cursor connections
def connect_db():
    db = oracle.connect("{}/{}@{}".format(credentials.username,
        credentials.password, credentials.server ))
    cursor = db.cursor()
    return db,cursor


# Closes SQL*Plus db and cursor connections
def close_db(db,cursor):
    cursor.close()
    db.close()


def add_data(table_name,data):
   loader.insert_data( table_name, data ) 


@app.route('/login', methods=['GET','POST'])
def login():
   return url_for('home')


@app.route('/register', methods=['GET','POST'])
def register():
    reg_form = forms.Register_Form(request.form)
    if request.method == 'POST' and reg_form.validate():
        user = [ reg_form.username.data, reg_form.password.data ]
        add_data('user_data',user)
        flash('Thanks for registering')
        return redirect( url_for('home') )
    return render_template('register.html', form=reg_form)


@app.route('/')
def home():
    return render_template( 'home.html' )



if __name__ == '__main__':
    app.run()
