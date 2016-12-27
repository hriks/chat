from flask import Flask, redirect, render_template,\
    request, url_for, flash, session
from db import db

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/logina', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        value = db.authenticate(
            request.form['username'],
            request.form['password'])
        if (value == 1):
            print "login Succesfully"
            session['name'] = request.form['username']
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
                data_chart=graph_data)
        else:
            error = 'Invalid username or password \
            Please try again!'
            return render_template('login.html', error=error, session=session)
    return render_template('login.html')


@app.route('/reg?is%2')
def registration():
    return render_template('registration.html')


@app.route("/registform", methods=['POST'])
def register():
    data = db.user_alreadyexits(request.form['field3'],
                                request.form['field1'],
                                request.form['field2'],
                                request.form['field4'])
    if (data == 1):
        flash('ERROR! PLEASE ENTER SOMETHING OR CHECK YOUR USER')
        return redirect(url_for('registration'))
    flash('You were successfull')
    return redirect(url_for('registration'))
