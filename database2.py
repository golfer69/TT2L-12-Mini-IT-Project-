from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def create_web():
    web = Flask(__name__)
    web.config['SECRET_KEY'] = 'chickenstuffe'
    return web

web=create_web()
web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.test'
web.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(web) # Initialise database

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Posts(db.Model):
    posts_id=db.Column(db.Integer, primary_key=True)
    image=db.Column(db.String(2000))
    posts_title=db.Column(db.String(20000), nullable=False)
    text=db.Column(db.String(20000), nullable=False)

# Creating a new user
new_user = User(user_id= 122, name='John Doe', email='john@example.com', date_posted=datetime.now)
db.session.add(new_user)

# Creating a new post
new_post = Posts(post_id= 990, image='chicken.jpg', posts_title='This is my first post', text='Hello world')
db.session.add(new_post)

# Committing the session to persist the changes to the database
db.session.commit()
db.session.close()