
from flask import Flask, render_template, flash, \
    url_for, redirect, request, session
import cx_Oracle as oracle
from scripts import credentials, loader, load_finance
from wtforms import Form, BooleanField, TextField, PasswordField, \
    validators, ValidationError, SelectField, TextAreaField, \
    IntegerField, DecimalField
from portfolio_calculations import controller

app = Flask(__name__)
app.config.from_object('flask_settings')


# Opens SQL*Plus db and cursor connections
def connect_db():
    db = oracle.connect("{}/{}@{}".format(credentials.username,
                                          credentials.password,
                                          credentials.server))
    cursor = db.cursor()
    return db, cursor


# Closes SQL*Plus db and cursor connections
def close_db(db, cursor):
    cursor.close()
    db.close()


def add_data(table_name, data):
    #print table_name
    #print data
    loader.insert_data(table_name, data)


def get_next_index(table_name, colum_name):
    sql_query = "SELECT MAX({}) FROM {}".format(colum_name,
                                                table_name)
    db, cursor = connect_db()
    cursor.execute(sql_query)
    max_index = int(cursor.fetchall()[0][0])
    return max_index+1


def check_if_logged_in():
    if 'user_id' not in session:
        flash('Please log in before making a strategy!')
        return redirect(url_for('log_in'))


def check_for_objects(table_name):
    sql_query = "SELECT COUNT(*) FROM {}".format(table_name)
    db, cursor = connect_db()
    cursor.execute(sql_query)
    num = int(cursor.fetchall()[0][0])
    close_db(db, cursor)
    return num


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html')


#####################################################################
# COOKIEZ
#####################################################################
def populate_cookie(user_id):
    db, cursor = connect_db()

    #get all strategies
    session.pop('strategy', None)
    cursor.execute("""  SELECT S.strategy_id, S.strategy_name
                        FROM create_strategy C, strategy S
                        WHERE C.strategy_id = S.strategy_id
                            AND C.user_id = '{}'
                        """.format(user_id))
    data = cursor.fetchall()
    if len(data) == 0:
        return
    only_strategy = data[0]
                        # Strategy ID,         Strat_name
    session['strategy'] = [(only_strategy[0], only_strategy[1])]
    print 'STRATEGY:', only_strategy, '\n'
    #session['strategy'] = [(only_strategy[0], unicode(only_strategy[1]))]
    # limiting to one strategy for now
    #strategies = []
    #for strat in data:
    #    print strat
    #    strategies.append((strat[0], unicode(strat[1])))
    #if len(strategies) > 0:
    #    session['strategy'] = strategies

    # get all indicators
    session.pop('indicator', None)
    indicators = []
    for strat in session['strategy']:
        cursor.execute("""  SELECT C.indicator_id, I.security,I.mva_10_day
                            FROM criteria C, indicator I
                            WHERE C.strategy_id = '{}'
                                AND C.indicator_id = I.indicator_id
                            """.format(strat[0]))
        for ind in cursor.fetchall():
            print ind
            if ind[2] is 'T':
                temp = '10 day'
            else:
                temp = '25 day'
            # Storing (indicator_id, ticker)
            indicators.append((ind[0], unicode("{} {}".format(ind[1], temp))))
    session['indicator'] = indicators
    print '\n', 'INDICATORS'
    for i in session['indicator']:
        print i

    session.pop('indicator_ref', None)
    indicator_references = []
    db, cursor = connect_db()
    for ind in indicators:
        sql_query = """
        SELECT DISTINCT
            R.L_indicator_id,
            R.R_indicator_id,
            R.buy_sell,
            R.operator
        FROM
            indicator I,
            indicator_reference R
        WHERE
            R.L_indicator_id = {0} OR
            R.R_indicator_id = {0}
        """.format(ind[0])
        cursor.execute(sql_query)
        data = cursor.fetchall()
        if len(data) > 0:
            for ind_ref in data:
                indicator_references.append(ind_ref)

    session['indicator_ref'] = indicator_references
    close_db(db, cursor)

    print '\n', 'TRIGGERS'
    for t in indicator_references:
        print t

    if 'trade' in session:
        print "IT'S IN THERE"


#####################################################################
# Create Forms
#####################################################################
def CreateForm(name, cookie_data=None):
    if name == 'indicator':
        class Create_Indicator_Form(Form):
            security = TextField('Ticker Name', [
                                 validators.Required(),
                                 validators.Length(min=1, max=6)])
            mva = SelectField('MVA',
                              choices=[('mva_10_day', u'10 Day'),
                                       ('mva_25_day', u'25 Day')])
            strategy = SelectField('strategy', choices=cookie_data,
                                   coerce=int)
        return Create_Indicator_Form(request.form)

    elif name is 'strategy':
        class Create_Strategy_Form(Form):
            strat_name = TextAreaField('Strategy Name', [
                                       validators.Required(),
                                       validators.Length(min=10, max=200)])
            cash = IntegerField('Starting cash amount', default=100000)

        return Create_Strategy_Form(request.form)

    elif name is 'login':
        class Log_In_Form(Form):
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
        return Log_In_Form(request.form)

    elif name is 'register':
        class Register_Form(Form):
            username = TextField('Username')
            password = PasswordField('New Password', [
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
        return Register_Form(request.form)

    elif name == 'indicator_ref':
        class Create_Indicator_Reference(Form):
            start_month = SelectField('Start Month', choices=[x for x in
                                      [('jan', 'January'), ('feb', 'February'),
                                      ('mar', 'March'), ('apr', 'April'),
                                      ('may', 'May'), ('jun', 'June'),
                                      ('jul', 'July'), ('aug', 'August'),
                                      ('sep', 'September'), ('oct', 'October'),
                                      ('nov', 'November'), ('dec', 'December')]])
            start_year = SelectField('Start Year', choices=[(x, x) for x in range(1900, 2013)],
                                     coerce=int)
            ind_1 = SelectField('Indicator 1', choices=cookie_data,
                                coerce=int)
            ind_2 = SelectField('Indicator 2', choices=cookie_data,
                                coerce=int)
            action = SelectField('Buy/Sell', choices=[('B', u'Buy'),
                                                      ('S', u'Sell')])
            operator = SelectField('Trigger', choices=[
                                   ('x_under', u'1 crosses under 2'),
                                   ('x_over', u'1 crosses over 2')])
            action_security = TextField('Action Security Ticker', [
                                        validators.Required(),
                                        validators.Length(min=1, max=6)])
            share_amount = IntegerField('Number of shares', default=0)
            allocation = DecimalField('Allocation (decimal)', default=0.0)
            cash_value = IntegerField('Cash Value', default=0)

        return Create_Indicator_Reference(request.form)


#####################################################################
# DO CRAZY BACKEND
#####################################################################
@app.route('/find_trades')
def find_trades():
    if session['trade'] != 'true':
        controller.backtest(session['strategy'][0][0])
    session['trade'] = 'true'
    return redirect(url_for('home'))


#####################################################################
# Show Aggregate Portfolios
#####################################################################
@app.route('/portfolio', methods=['GET'])
def show_portfolio():
    check_if_logged_in()
    populate_cookie(session['user_id'])
    # Query finds all relevant aggregate portfolios
    sql_query = """SELECT
        A.time,
        A.portfolio_value,
        A.securites_value,
        A.free_cash,
        A.portfolio_value_change
    FROM
        day_to_day D,
        aggregate_portfolio A
    WHERE
        D.strategy_id = {} AND
        D.portfolio_id = A.portfolio_id
    """.format(session['strategy'][0][0])
    db, cursor = connect_db()
    cursor.execute(sql_query)
    data = cursor.fetchall()
    close_db(db, cursor)
    print 'PORTFOLIO VALUES'
    for day in data:
        print day
    return render_template('portfolio.html', portfolios=data)


#####################################################################
# Show Trades
#####################################################################
@app.route('/trades', methods=['GET'])
def show_trades():
    check_if_logged_in()
    populate_cookie(session['user_id'])
    strat_id = session['strategy'][0][0]

    # Should return on the current strategies trades
    sql_query = """SELECT
        T.security,
        T.action,
        T.share_amount,
        T.allocation,
        T.price,
        T.time
    FROM
        day_to_day D,
        makes_trade M,
        trade T
    WHERE
        D.strategy_id = {} AND
        D.portfolio_id = M.portfolio_id AND
        T.trade_id = M.trade_id
    ORDER BY
        T.time
    """.format(strat_id)

    print 'SQL QUERY\n', sql_query
    db, cursor = connect_db()
    cursor.execute(sql_query)
    data = cursor.fetchall()
    print 'HERE ARE THE TRADES'
    print data
    close_db(db, cursor)

    return render_template('trades.html', trades=data)


#####################################################################
# Create Indicator Reference
#####################################################################
@app.route('/indicator_reference', methods=['GET', 'POST'])
def indicator_reference():
    check_if_logged_in()

    populate_cookie(session['user_id'])
    print session['indicator']
    indicator_ref = CreateForm('indicator_ref', session['indicator'])

    if request.method == 'POST' and indicator_ref.validate():

        # If the indicators are identical
        if indicator_ref.ind_1.data == indicator_ref.ind_2.data:
            flash('You must choose two different indicators!')
            return render_template('indicator_reference.html',
                                   form=indicator_ref)

        start_date = '01-{}-{}'.format(indicator_ref.start_month.data,
                                       str(indicator_ref.start_year.data))
        row = [start_date,
               '01-mar-2013',
               indicator_ref.ind_1.data,
               indicator_ref.ind_2.data,
               indicator_ref.action.data,
               indicator_ref.operator.data,
               indicator_ref.action_security.data,
               indicator_ref.share_amount.data,
               indicator_ref.allocation.data,
               indicator_ref.cash_value.data]

        # Inserting the relations data
        add_data('indicator_reference', row)
        flash('Your new trigger has been created!')
        if 'indicator_ref' in session:
            session['indicator_ref'].append((indicator_ref.ind_1.data,
                                             indicator_ref.ind_2.data,
                                             indicator_ref.action.data))
        else:
            session['indicator_ref'] = [(indicator_ref.ind_1.data,
                                         indicator_ref.ind_2.data,
                                         indicator_ref.action.data)]
        # Trying to upload the action security to the databse
        load_finance.upload_ticker(indicator_ref.action_security.data)
        return redirect(url_for('home'))

    return render_template('indicator_reference.html',
                           form=indicator_ref)


#####################################################################
# Create Indicator
#####################################################################
@app.route('/create_indicator', methods=['GET', 'POST'])
def create_indicator():
    check_if_logged_in()
    create_indicator_form = CreateForm('indicator', session['strategy'])
    #print session['strategy']

    if request.method == 'POST' and create_indicator_form.validate():
        indicator_id = get_next_index('indicator', 'indicator_id')
        ticker = create_indicator_form.security.data
        print 'HERE', create_indicator_form.mva.data
        if create_indicator_form.mva.data == 'mva_10_day':
            mva_10_day = 'T'
            mva_25_day = 'F'
        else:
            mva_10_day = 'F'
            mva_25_day = 'T'
        row = [indicator_id, ticker, mva_10_day, mva_25_day]
        add_data('indicator', row)
        # adding relation
        criteria_row = [create_indicator_form.strategy.data, indicator_id]
        add_data('criteria', criteria_row)
        # adding to session
        if 'indicator' in session:
            print 'ind in session'
            session['indicator'].append((indicator_id,
                                        u'{} {}'.format(ticker,
                                        create_indicator_form.mva.data)))
        else:
            session['indicator'] = [(indicator_id,
                                    u'{} {}'.format(ticker,
                                    create_indicator_form.mva.data))]
        print session['indicator']
        # Trying to upload ticker to the database
        load_finance.upload_ticker(ticker)
        return redirect(url_for('home'))

    return render_template('create_indicator.html',
                           form=create_indicator_form)


#####################################################################
# Create Strategy
#####################################################################
@app.route('/create_strategy', methods=['GET', 'POST'])
def create_strategy():
    check_if_logged_in()
    create_strat_form = CreateForm('strategy')

    if request.method == 'POST' and create_strat_form.validate():
        strat_id = get_next_index('strategy', 'strategy_id')
        strat_name = create_strat_form.strat_name.data
        cash = create_strat_form.cash.data
        strat = [strat_id, strat_name, cash]
        add_data('strategy', strat)
        add_data('create_strategy', [session['user_id'], strat_id])

        if 'strategy' in session:
            session['strategy'].append((strat_id, strat_name))
        else:
            session['strategy'] = [(strat_id, strat_name)]
        flash('New strategy, {}, created'.format(strat_name))
        return redirect(url_for('home'))

    return render_template('create_strategy.html',
                           form=create_strat_form)


#####################################################################
# Log In
#####################################################################
@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    log_in_form = CreateForm('login')

    if request.method == 'POST' and log_in_form.validate():
        session['user_id'] = log_in_form.username.data
        flash("You're logged in as {}".format(session['user_id']))
        populate_cookie(log_in_form.username.data)
        return redirect(url_for('home'))

    return render_template('log_in.html', form=log_in_form)


#####################################################################
#Register User
#####################################################################
@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = CreateForm('register')

    if request.method == 'POST' and reg_form.validate():
        user = [reg_form.username.data, reg_form.password.data]
        add_data('user_data', user)
        flash('Thanks for registering, {}'.format(user[0]))
        return redirect(url_for('home'))

    return render_template('register.html', form=reg_form)


#####################################################################
# Log Out
#####################################################################
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


#####################################################################
# Home
#####################################################################
@app.route('/')
def home():
    if 'user_id' in session:
        populate_cookie(session['user_id'])
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
