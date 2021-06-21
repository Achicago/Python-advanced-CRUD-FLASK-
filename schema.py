import sqlite3

connection = sqlite3.connect('cyfa.db', check_same_thread=False)
cursor = connection.cursor()

# cursor.execute(
#     """CREATE TABLE users(
#         pk  INTEGER PRIMARY KEY AUTOINCREMENT,
#         username VARCHAR(16),
#         email VARCHAR(50),
#         password VARCHAR(32),
#         favorite_color VARCHAR(32),
#         image VARCHAR(32)
#     );"""
# )

cursor.execute(
    """CREATE TABLE product(
        pid  INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(200),
        description TEXT,
        userID INTERGER,
        date_time  VARCHAR(32),
        product_image VARCHAR(32)
    );"""
)

connection.commit()
cursor.close()
connection.close()
