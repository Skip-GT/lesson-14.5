import sqlite3


def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def init_db():
    connn = sqlite3.connect('Users.db')
    cursor = connn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                balance INTEGER NOT NULL DEFAULT 1000
            )
        ''')

    connn.commit()
    connn.close()


def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, description, price FROM Products')
    products = cursor.fetchall()
    conn.close()
    return products


def add_user(username, email, age):
    connn = sqlite3.connect('Users.db')
    cursor = connn.cursor()
    cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', (username, email, age))
    connn.commit()
    connn.close()


def is_included(username):
    connn = sqlite3.connect('Users.db')
    cursor = connn.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()
    connn.close()
    return user is not None


"""def populate_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    products = [
        ('Витамин А', 'для зрения, роста, деления клеток и иммунитета.', 100),
        ('Витамин С', 'укрепляет десны, зубы и сосуды.', 200),
        ('Витамин D3', 'регулирует обмен кальция и фосфора.', 300),
        ('Витамин B', 'для обмена веществ и функционирования нервной системы.', 400)
    ]

    cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', products)
    conn.commit()
    conn.close()"""