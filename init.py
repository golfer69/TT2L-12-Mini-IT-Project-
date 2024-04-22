from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

def add_new_user(user_id,name, email, date_posted):
    with app.app_context():
        new_user = User(user_id=user_id, name=name, email=email, date_posted=date_posted)
        db.session.add(new_user)
        db.session.commit()

# Now you can call the function to add a new user
add_new_user(122110, 'John Doe', 'john@example.com', datetime.now)
