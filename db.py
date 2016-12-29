import psycopg2 as pg


def get_connection():
    conn = pg.connect(
        database='pghmpgde',
        user='pghmpgde',
        password='o_QTqNZ0fagtZmjdc9NsUnBW-S3OKgFP',
        host='elmer-02.db.elephantsql.com',
        port=5432)
    return conn


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


def add_friend(friend_name):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """CREATE TABLE %s(USERID       TEXT   REFERENCES LOGS(USERID)  NOT Null,
                                  REFERRALID  TEXT   REFERENCES LOGS(REFERRALID) NOT NULL,
                                  CHAT            TEXT     NOT NULL);"""
        query = query % (friend_name)
        cursor.execute(query)
        print "Friend connected successfully"
        connection.commit()
        connection.close()
    except Exception as e:
        return e


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


def authenticate_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT USERID, PASSWORD from LOGS
     where USERID='%s' and PASSWORD='%s';"""
    query = query % (username, password)
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    try:
        if (rows[0][0] == username) and (rows[0][1] == password):
            return 1
        else:
            return 0
    except Exception as e:
        return e
