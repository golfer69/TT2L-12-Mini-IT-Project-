from flask import Flask
import sqlite3
from datetime import datetime

conn=sqlite3.Connection('User.db')
cur=conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS user_data(Name, ID PRIMARY KEY, Email UNIQUE, DATE_POSTED)
                   """)

def insert_data(name, user_id, email, date_posted):
    cur.execute("""INSERT INTO user_data(Name, ID, Email, Date_Posted) VALUES(?, ?, ?, ?)""",  (name, user_id, email, date_posted ))
    conn.commit()


def pull_data():
    cur.execute('''SELECT * FROM user_data''')
    return cur.fetchall()

def validate_input_length(input_str, max_length):
    return input_str[:max_length]

# User details
while True:
    name = input('Enter your name: ')
    if len(name) > 100:
        print("Name must be 100 characters or fewer. Please try again.")
    else:
        break
user_id=int(input('Enter id: ' ))
while True:
    email = input('Enter your name: ')
    if len(email) > 150:
        print("Name must be 150 characters or fewer. Please try again.")
    else:
        break  
date_posted=datetime.now()


insert_data(name, user_id, email, date_posted)
data=pull_data()

print("Name\tID\tEMAIL\tDATE_POSTED")
for row in data:
    print("{}\t{}\t{}\t{}".format(row[0], row[1], row[2], row[3]))
