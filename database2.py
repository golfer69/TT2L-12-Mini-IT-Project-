# import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create web
web = Flask(__name__)
# create database
web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Initialise database
db = SQLAlchemy(web)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

db.create_all()
