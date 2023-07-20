import mysql.connector
from mysql.connector import Error

def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo


def renew_resume(dob,fromloc,fromto,passform,passto,filename,name):
    data = read_file(filename)

    query = "UPDATE newpass SET dob = '%s', fromloc = '%s', fromto = '%s', passform = '%s', passto = '%s', filename = '%s' WHERE name = %s;"

    args = (dob,fromloc,fromto,passform,passto,data,name)


    try:
        conn = mysql.connector.connect(host='127.0.0.1', user='root', password='', database='smartbuspass')
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


