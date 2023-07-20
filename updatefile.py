import mysql.connector
from mysql.connector import Error

def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo


def update_blob(pass_id, filename):
    data = read_file(filename)

    query = "UPDATE newpass " \
            "SET profile = %s " \
            "WHERE passid  = %s"

    args = (data, pass_id)


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

# update_blob(574718, "DSC_3235.JPG")
