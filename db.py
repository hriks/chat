import psycopg2 as pg


def get_connection():
    conn = pg.connect(
        database='pghmpgde',
        user='pghmpgde',
        password='o_QTqNZ0fagtZmjdc9NsUnBW-S3OKgFP',
        host='elmer-02.db.elephantsql.com',
        port=5432)
    return conn


def create_db():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE LOGS
        (USERID       TEXT    UNIQUE    NOT Null,
         NAME           TEXT    NOT NULL,
         EMAIL            TEXT     NOT NULL,
         PASSWORD        TEXT);''')
        print "Table created successfully"
        cursor.execute('''CREATE TABLE LOGSS
         (USERID       TEXT   REFERENCES LOGS(USERID)  NOT Null,
            CATAGORIES           TEXT   UNIQUE   NOT NULL,
             PRICE            INT     NOT NULL,
            DESCRIPTION        TEXT);''')
        connection.commit()
        connection.close()
    except Exception as error:
        return error


def register_me_input(USERID, REFRALID, NAME, EMAIL, PHONENO, PASSWORD):
    connection = get_connection()
    cursor = connection.cursor()
    print "cur is created"
    query = """INSERT INTO LOGS(USERID,REFERRALID,NAME,EMAIL,PHONE,PASSWORD) VALUES('%s', '%s', '%s', '%s', %s, '%s');"""
    query = query % (
        USERID, REFRALID, NAME, EMAIL, PHONENO, PASSWORD)
    print query
    cursor.execute(query)
    connection.commit()
    print "Records created successfully"
    connection.close()


def register_me(USERID, REFRALID, NAME, EMAIL, PHONENO, PASSWORD):
    connection = get_connection()
    print "connection created"
    cursor = connection.cursor()
    query = """SELECT USERID from LOGS where USERID='%s';"""
    query = query % (USERID)
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    print rows
    try:
        if (len(rows) == 0):
            register_me_input(USERID, REFRALID, NAME, EMAIL, PHONENO, PASSWORD)
            return 1
        else:
            return 0
    except Exception as error:
        return error


def filter_user_data(USER):
    connection = get_connection()
    cursor = connection.cursor()
    fetch_db = """SELECT USERID, CATAGORIES, PRICE,
     DESCRIPTION  from LOGSS where USERID='%s'"""
    fetch_db = fetch_db % (USER)
    cursor.execute(fetch_db)
    rows = cursor.fetchall()
    print "Operation done successfully"
    cursor.close()
    return rows


def insert_db(USER, NAME, EMAIL, PASSWORDV):
    connection = get_connection()
    cursor = connection.cursor()
    print "cur is created"
    query = """INSERT INTO LOGS(USERID,NAME,
    EMAIL,PASSWORD) VALUES('%s', '%s', '%s', '%s');"""
    query = query % (
        USER, NAME, EMAIL, PASSWORDV)
    print query
    cursor.execute(query)
    connection.commit()
    print "Records created successfully"
    connection.close()


def user_alreadyexits(USER, NAME, EMAIL, PASSWORDV):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT USERID from LOGS where USERID='%s';"""
    query = query % (USER, )
    cursor.execute(query)
    rows = cursor.fetchall()
    try:
        if (len(rows) == 0):
            insert_db(USER, NAME, EMAIL, PASSWORDV)
        else:
            return 1
    except Exception as error:
        return error
    connection.close()


def authenticate(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT USERID, PASSWORD from LOGS
     where USERID='%s' and PASSWORD='%s';"""
    query = query % (username, password)
    cursor.execute(query)
    rows = cursor.fetchall()
    try:
        if (rows[0][0] == username) and (rows[0][1] == password):
            return 1
        else:
            return 0
    except Exception as error:
        return error
    connection.close()
