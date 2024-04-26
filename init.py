from flask import Flask
import sqlite3
<<<<<<< Updated upstream

=======
from datetime import datetime

conn=sqlite3.Connection('User.db')
cur=conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS user_data(Name, ID PRIMARY KEY, Email UNIQUE, DATE_POSTED)
                   """)

# User_Details:
name=input('Enter your name: ')
user_id=int(input('Enter id: ' ))
email=input('Enter email: ')
date_posted=datetime.now()



def insert_data(name, user_id, email, date_posted):
    cur.execute("""INSERT INTO user_data(Name, ID, Email, Date_Posted) VALUES(?, ?, ?, ?)""",  (name, user_id, email, date_posted ))
    conn.commit()


def pull_data():
    cur.execute('''SELECT * FROM user_data''')
    return cur.fetchall()   

insert_data(name, user_id, email, date_posted)
data=pull_data()

print("Name\tID\tEMAIL\tDATE_POSTED")
for row in data:
    print("{}\t{}\t{}\t{}".format(row[0], row[1], row[2], row[3]))
>>>>>>> Stashed changes
