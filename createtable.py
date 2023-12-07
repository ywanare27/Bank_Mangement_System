from flask import Flask, request
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect('demo.db')
cursor = connection.cursor()



cursor.execute('CREATE TABLE IF NOT EXISTS users (userID NUMERIC PRIMARY KEY,'
               'userName TEXT UNIQUE NOT NULL,'
               'password TEXT NOT NULL,'
               'userRole TEXT NOT NULL) ')



cursor.execute('PRAGMA foreign_keys = ON;')


cursor.execute('CREATE TABLE IF NOT EXISTS transactions ('
               'transactionID NUMERIC PRIMARY KEY, '
               'transactionDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
               'transactionType TEXT NOT NULL,'
               'amount NUMERIC NOT NULL ,'
               'party1ID NUMERIC ,'
               'party2ID NUMERIC,'
               'transactionStatus TEXT DEFAULT "Pending" ,'
               'category TEXT,'
               'comments TEXT,'
               'CONSTRAINT fk_Party1 FOREIGN KEY (party1ID) REFERENCES users(userID),'
               'CONSTRAINT fk_Party2 FOREIGN KEY (party2ID) REFERENCES users(userID)'
               ')')

connection.close()


@app.route('/show_users')
def showUser():
    connection = sqlite3.connect('demo.db')
    cursor = connection.cursor()
    data = {"User List ": list(cursor.execute('SELECT * FROM users'))}
    connection.close()
    return data


@app.route('/enter_user', methods=['POST'])
def register():
    data = request.get_json()
    connection = sqlite3.connect("demo.db")
    cursor = connection.cursor()

    try:
        cursor.execute('INSERT INTO users(userID, userName, password, userRole) VALUES(?,?,?,?)',
                       (data["id"], data["name"], data["pass"], data["role"]))
        connection.commit()
        return 'User is registered...'

    except sqlite3.Error as e:
        return f"Error inserting data: {str(e)}"

    finally:
        if connection:
            connection.close()


@app.route('/enter_transaction', methods=["POST"])
def transaction_entry():
    data = request.get_json()
    connection = sqlite3.connect('demo.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            'INSERT INTO transactions(transactionID ,transactionType ,amount, party1ID,party2ID, category,comments ) VALUES (?,?,?,?,?,?,?)',
            (data["tID"], data["tType"], data["amount"], data["party1"], data["party2"], data["cat"], data["comment"]))
        connection.commit()

        return 'transaction recorded successfully'
    except sqlite3.Error as e:
        return f"Error in inserting data: {str(e)}"

    finally:
        if connection:
            connection.close()


@app.route('/show_transaction')
def show_trans():
    connection = sqlite3.connect('demo.db')
    cursor = connection.cursor()

    res = {"Transaction": list(cursor.execute('SELECT * FROM transactions'))}
    connection.close()
    return res


app.run(port=3333)
