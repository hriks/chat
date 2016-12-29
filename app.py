from flask import Flask, redirect, render_template,\
    request, url_for, flash, session
from db import *

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jfmM]Lwf/,?KT'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/log')
def log():
    return render_template('index.html')


@app.route('/logina', methods=['GET', 'POST'])
def logina():
    error = None
    if request.method == 'POST':
        value = authenticate_user(
            request.form['username'],
            request.form['password'])
        if (value == 1):
            print "login Succesfully"
            session['name'] = request.form['username']
            return render_template('logged.html', session=session)
        else:
            error = 'Invalid username or password \
            Please try again!'
            return render_template('index.html', error=error, session=session)
    return render_template('logged.html', error=error)


@app.route('/friend', methods=['POST'])
def friend():
    error_user = None
    if request.method == 'POST':
        print request.form['friendname']
        user_value = add_friend(request.form['friendname'])
        print user_value, error_user
        return render_template('logged.html')


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/reg?me?chat2')
def registration():
    return render_template('register.html')


@app.route('/contact?me')
def contact():
    return render_template('contactus.html')


@app.route('/registerme', methods=['POST'])
def registerme():
    data = register_me(request.form['userid'],
                       request.form['referralid'],
                       request.form['fullname'],
                       request.form['emailid'],
                       request.form['phone'],
                       request.form['password'])
    if (data == 1):
        return render_template('register.html')
    else:
        return render_template('register.html')
    return render_template('register.html')


@app.route('/loggeds')
def index():
    error = None
    try:
        user_data = session['name']
        print user_data
        data = db.filter_user_data(user_data)
        data_user_get = db.filter_user_chart(user_data)
        graph_data = []
        for elem in data_user_get:
            cat = elem[0]
            exp = elem[1]
            li = [cat, int(exp)]
            graph_data.append(li)
        graph_data.insert(0, ['Category', 'Expenses'])
        return render_template(
            'index.html',
            error=error,
            data=data,
            data_chart=graph_data,
            session=session)
    except Exception as e:
        raise e


@app.route('/password??')
def password_help():
    return render_template('forgot_pass.html')


@app.route('/logged')
def user_page():
    return render_template('logged.html')


@app.route('/faq??')
def faq():
    return render_template('faq.html')


@app.route('/asd')
def data_user():
    error = None
    data = None
    if session['name']:
        user_data = session['name']
        print user_data
        data = db.filter_user_data(user_data)
        return render_template('index.html', error=error, data=data)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('log'))


if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int("8080")
    )
