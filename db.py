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


def add_friend(friend_name, uuserid, fuserid, refferalid):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = ('''CREATE TABLE %s
        (%s       TEXT      ,
        %s           TEXT   ,
        %s            TEXT  ,
        CHAT      TEXT       NOT NULL);''')
        query = query % (friend_name, uuserid, fuserid, refferalid)
        print query
        cursor.execute(query)
        print "Friend connected successfully"
        connection.commit()
        connection.close()
        return 1
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


def chat_data(name):
    connection = get_connection()
    cursor = connection.cursor()
    fetch_db = """SELECT CHAT  from %s;"""
    fetch_db = fetch_db % (name)
    cursor.execute(fetch_db)
    rows = cursor.fetchall()
    print "Operation done successfully"
    cursor.close()
    return rows


def friend_data(user_name):
    connection = get_connection()
    cursor = connection.cursor()
    query = """select * from INFORMATION_SCHEMA.COLUMNS where COLUMN_NAME = '%s' order by TABLE_NAME"""
    query = query % (user_name)
    cursor.execute(query)
    rows = cursor.fetchall()
    print "Operation done successfully"
    cursor.close()
    return rows


def send_chat(TABLE, MESSAGE):
    connection = get_connection()
    cursor = connection.cursor()
    query = """INSERT INTO %s(CHAT) VALUES('%s');"""
    query = query % (
        TABLE, MESSAGE)
    print query
    cursor.execute(query)
    connection.commit()
    print "Message Send created successfully"
    connection.close()      
# query used for chatting with friends
