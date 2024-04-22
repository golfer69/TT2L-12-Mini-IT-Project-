from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database2 import db, User, Posts, web

# Routes
@web.route('/add_data')
def add_data():
    print("Adding data...")
    new_user = User(name='John Doe', email='john@example.com')
    new_posts= Posts(image='chicken', posts_title='stuff',text='nobody cares')
    db.session.add(new_user)
    db.session.add(new_posts)
    db.session.commit()
    db.session.close()
    print('data added successfully')
    return 'Entry added'