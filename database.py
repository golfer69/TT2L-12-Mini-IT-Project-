import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


connection=sqlite3.Connection('User.db')
cursor=connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS user_data(Name, ID PRIMARY KEY, Age INTEGER)
                   """)


user_name=input('Enter your name: ')
id_number=int(input('Enter id: ' ))
age=int(input('Enter age: '))


def insert_data(user_name, age, id_number):
    cursor.execute("""INSERT INTO user_data(Name, ID, Age) VALUES(?, ?, ?)""",  (user_name, id_number, age))
    connection.commit()


def pull_data():
    cursor.execute('''SELECT * FROM user_data''')
    return cursor.fetchall()   

insert_data(user_name, age, id_number)
data=pull_data()

print("Name\tID\tAge")
for row in data:
    print("{}\t{}\t{}".format(row[0], row[1], row[2]))

ap='chicken is good'
