
from flask import Flask, render_template, flash, \
	url_for, g, redirect
import forms


app = Flask(__name__)
app.config.from_object('flask_settings')

@app.route('/register', methods=['GET','POST']):
def register():
    reg_form = forms.Register_Form(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.password.data)
        flash('Thanks for registering')
        return redirect( url_for('login'))
    return render_template('register.html', form=reg_form)


@app.route('/')
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.run()
