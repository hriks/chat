from flask import Flask, redirect, render_template,\
    request, url_for, flash, session
import db

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/create_db')
def create_db():
    db.create_db()
    return "created"


@app.route('/log?usr?get', methods=['GET', 'POST'])
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
                data=data)
        else:
            error = 'Invalid username or password \
            Please try again!'
            return render_template('logged.html', error=error, session=session)
    return render_template('logged.html')


@app.route('/reg?me?chat2')
def registration():
    return render_template('register.html')


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


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/clearsession')
def clearsession():
    session.clear()
    return redirect(url_for('logina'))


@app.route('/future')
def future():
    return render_template('upcoming.html')


@app.route('/logina')
def logina():
    return render_template('login.html')


@app.route('/add')
def add():
    return render_template('add_catagories.html')


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


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


@app.errorhandler(500)
def special_exception_handler(error):
    return ' Unuthorized Database connection failed', 500


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80")
    )
