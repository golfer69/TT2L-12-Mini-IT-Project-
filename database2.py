from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app
from werkzeug.utils import secure_filename
import os 

# create web
# def create_web():
#     web = Flask(__name__)
#     web.config['SECRET_KEY'] = 'chickenstuffe'
#     return web

# web = create_web()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # create database
db = SQLAlchemy(app) # Initialise database

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

def create_tables():
    db.create_all()

@app.route('/add_user', methods=['POST'])
def add_user():
    name= request.form['name']
    email=request.form

    new_user= User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']
    image = request.form.get('image', None)  # You may need to adjust this depending on how you handle file uploads
    
    new_post = Posts(title=title, content=content, image=image)
    db.session.add(new_post)
    db.session.commit()
    
    return redirect('/')


if __name__ == "__main__":
    # Call the function to create tables
    create_tables()
    # Run the Flask app
    app.run(debug=True)

