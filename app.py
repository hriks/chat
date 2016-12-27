from flask import Flask, redirect, render_template,\
    request, url_for, flash, session
import db

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jfmM]Lwf/,?KT'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/log?usr?get', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        value = db.authenticate(
            request.form['username'],
            request.form['password'])
        if (value == 1):
            print "login Succesfully"
            return render_template(
                'logged.html',
                error=error)
        else:
            error = 'Invalid username or password \
            Please try again!'
            return render_template('logged.html', session=session)
    return render_template('logged.html')


@app.route('/reg?me?chat2')
def registration():
    return render_template('register.html')


@app.route('/contact?me')
def contact():
    return render_template('contactus.html')


@app.route('/register', methods=['POST'])
def register():
    a = request.form['userid']
    dataaa = db.register_me(request.form['referralid'], request.form['name'], request.form['email'], request.form['phone'], request.form['password'])
    if (dataaa == 1):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    return redirect(url_for('registration'))


@app.route('/login')
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


@app.route('/add')
def add():
    return render_template('add_catagories.html')


@app.route('/password??')
def password_help():
    return render_template('forgot_pass.html')


@app.route('/faq??')
def faq():
    return render_template('faq.html')


@app.route("/catagory", methods=['POST'])
def catagory():
    error = None
    data_catagory = db.catagory_alreadyexits(session['name'],
                                             request.form['field7'],
                                             request.form['field8'],
                                             request.form['field9'])
    if (data_catagory == 1):
        flash('ERROR! CATAGORY ALREADY SATISFIED OR SOMETHING WENT WRONG PLEASE CHECK NEXT MESSAGE TO CONFIRM')
    else:
        flash(data_catagory)
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
    flash('REQUEST PERFORMED!')
    return redirect('add')


@app.route('/asd')
def data_user():
    error = None
    data = None
    if session['name']:
        user_data = session['name']
        print user_data
        data = db.filter_user_data(user_data)
        return render_template('index.html', error=error, data=data)


if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int("8080")
    )
