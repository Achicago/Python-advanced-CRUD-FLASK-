import sqlite3
# import os
# from werkzeug.utils import secure_filename
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def check_users():
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT username FROM users ORDER BY pk DESC;""")
    db_users = cursor.fetchall()
    users = []
    if db_users is None:
        return None
    else:
        for i in range(len(db_users)):
            person = db_users[i][0]
            users.append(person)
    connection.commit()
    cursor.close()
    connection.close()
    return users


def VerifyEmail(email):
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT email FROM users WHERE email='{mail}'; """.format(mail=email))
    exist = cursor.fetchone()
    if exist is None:
        return None
    return True


def VeryfyEmail(email):
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM users WHERE email='{mail}'; """.format(mail=email))
    user = cursor.fetchone()
    if user is None:
        return None
    return user


def CreateAccount(email, password, img):
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" INSERT INTO users(email, password, image)VALUES('{email}', '{password}', '{img}');""".format(email=email, password=password, img=img))
    connection.commit()
    cursor.close()
    connection.close()
    return True


def VerifyUser(email):
    connection = sqlite3.connect('cyfa.db')
    cursor = connection.cursor()
    query = "SELECT * FROM {table} WHERE email=?".format(table='users')
    result = cursor.execute(query, (email,))
    row = result.fetchone()
    if row is None:
        return None
    connection.commit()
    cursor.close()
    connection.close()
    return row


def UpdateUserName(username, id):
    connection = sqlite3.connect('cyfa.db', check_same_thread=False)
    cursor = connection.cursor()
    query = "UPDATE {table} set username=? WHERE pk=? ".format(table='users')
    cursor.execute(query, (username, id))
    connection.commit()
    cursor.close()
    connection.close()
    return True

#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# def UploadFile():
#     if 'file' not in file.files:
#         return render_template('create-account.html', msg='No file part')
#     file = file.files['file']
#     if file.filename == '':
#         return render_template('create-account.html', msg='No image selected for uploading')
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return render_template('create-account.html', msg='No image selected for uploading')
#     else:
#         return render_template('create-account.html', msg='Allowed image types are -> png, jpg, jpeg, gif')
#
#     return secure_filename(file.filename)
