# import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



# create web
web= Flask(__name__)
# create database
web.config['sqlalchemy_database_uri']= 'sqlite:///users.db'
# Initialise database
db= SQLAlchemy(web)

class users(db.model):
    id= db.column(db.integer, primary_key=True, nullable=False)
    name= db.column(db.string(150), nullable=False)
    email= db.column(db.string(100), nullable=False, unique=True)
    date_posted= db.column(db.datetime, nullable=False)

db.create_all()