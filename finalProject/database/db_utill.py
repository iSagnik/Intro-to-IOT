from database import dbInfo
import psycopg2
import logging
import pickle

db = "user=%s password=%s host=%s port=%s dbname=%s" % (
    dbInfo.user, dbInfo.password, dbInfo.host, dbInfo.port, dbInfo.database_name)

def addEntry(table, name, face_data):
    if not checkTableName(table):
        logging.error("Incorrect table name: " + table)
        return False
    # connect to the PostgreSQL database
    conn = psycopg2.connect(db)
    # create a new cursor
    cur = conn.cursor()
    table_name = table
    sql_temp = f"INSERT INTO {table_name}(name, faceData) VALUES"
    sql = sql_temp + """(%s, %s)"""
    return_val = True
    try:
        cur.execute(sql, (name, pickle.dumps(face_data)))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(str(error))
        print(str(error))
        return_val = False
    finally:
        if conn is not None:
            cur.close()
            conn.close()  
    return return_val

def getEntries(table):
    if not checkTableName(table):
        logging.error("Incorrect table name: " + table)
        return False
    # connect to the PostgreSQL database
    conn = psycopg2.connect(db)
    # create a new cursor
    cur = conn.cursor()
    table_name = table
    sql = f"SELECT * FROM {table_name}"

    try:
        # execute the SELECT statement
        cur.execute(sql)
        # store all data from the table
        sqlData = cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(str(error))
        sqlData = False
    finally:
        if conn is not None:
            cur.close()
            conn.close()

    #some_array = pickle.loads(cursor.fetchone()[0])
    return sqlData

def removeEntry(table, name):
    if not checkTableName(table):
        logging.error("Incorrect table name: " + table)
        return False
    # connect to the PostgreSQL database
    conn = psycopg2.connect(db)
    # create a new cursor
    cur = conn.cursor()
    table_name = table
    sql = f"DELETE FROM {table_name} WHERE name = '{name}';"
    return_val = True
    try:
        # execute the SELECT statement
        cur.execute(sql)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(str(error))
        return_val = False
    finally:
        if conn is not None:
            cur.close()
            conn.close()
    return return_val

def clearAll():
    # connect to the PostgreSQL database
    conn = psycopg2.connect(db)
    # create a new cursor
    cur = conn.cursor()
    tables = ["Owners", "Guests", "Outlaws"]

    try:
        # execute the SELECT statement
        for table in tables:
            sql = f"DELETE FROM {table};"
            cur.execute(sql)
            conn.commit()
        return_val = True

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(str(error))
        return_val = False
    finally:
        if conn is not None:
            cur.close()
            conn.close()
    return return_val

def checkTableName(table):
    if table != 'Owners' and table != 'Guests' and table != 'Outlaws':
        return False
    return True