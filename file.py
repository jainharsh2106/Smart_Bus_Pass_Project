import mysql.connector
from tkinter import *
from mysql.connector import Error

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def read_blob(pass_id, filename):
    query = "SELECT profile FROM newpass WHERE passid = %s"

    try:
        conn = mysql.connector.connect(host='127.0.0.1', user='root', password='', database='smartbuspass')
        cursor = conn.cursor()
        cursor.execute(query, (pass_id,))
        photo = cursor.fetchone()[0]
        write_file(photo, filename)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
      
# read_blob(574718,"read.jpg")