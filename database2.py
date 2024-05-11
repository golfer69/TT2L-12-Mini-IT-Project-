from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from app import app
import app
from werkzeug.utils import secure_filename
import os 

# def create_web():
#     web = Flask(__name__)
#     web.config['SECRET_KEY'] = 'chickenstuffe'
#     web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#     return web

db = SQLAlchemy(app) # Initialise database
if __name__ == "__main__":
    app.run(debug=True)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Posts(db.Model):
    posts_id=db.Column(db.Integer, primary_key=True)
    image=db.Column(db.String(2000))
    title=db.Column(db.String(20000), nullable=False)
    text=db.Column(db.String(20000), nullable=False)

# Creating a new user
new_user = User(name='John Doe', email='john@example.com')
# Adding the new user to the session
db.session.add(new_user)

# Creating a new post
new_post = Posts(title='Hello World', content='This is my first post.', date_posted=datetime.now())
# Adding the new post to the session
db.session.add(new_post)

# Committing the session to persist the changes to the database
db.session.commit()
db.session.close()




