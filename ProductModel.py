import sqlite3
from datetime import date
today = date.today()


def AddItem(name, des, file, userID):
    date = today.strftime("%b-%d-%Y : %S:%M:%H")
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()

    query = "INSERT INTO {table} (name, description, userID, date_time, product_image) VALUES(?, ?, ?, ?, ?)".format(table='product')
    cursor.execute(query, (name, des, userID, date, file))

    connection.commit()
    connection.close()
    return True


def UpdateItem(name, des, _id):
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()
    query = "UPDATE {table} SET name=?, description=? WHERE pid=?".format(table='product')
    cursor.execute(query, (name, des, _id))
    connection.commit()
    connection.close()
    return True


def AllItem():
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM {table} ORDER BY pid ASC;""".format(table='product'))
    db_product = cursor.fetchall()
    products = []
    if db_product is None:
        return None
    else:
        for i in range(len(db_product)):
            person = db_product[i][0]
            products.append(person)
    connection.commit()
    cursor.close()
    connection.close()

    return db_product


def GetItemById(_id):
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM {table} WHERE pid = {id} ;""".format(table='product', id = _id))
    product = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return product


def GetItemName(name):
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM {table} WHERE name = {name} ;""".format(table='product', name = name))
    product = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return product


def DeleteProduct(_id):
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" DELETE FROM {table} WHERE pid = {id};""".format(table='product', id = _id))
    connection.commit()
    cursor.close()
    connection.close()
    return True
