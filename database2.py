from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create web
# def create_web():
#     web = Flask(__name__)
#     web.config['SECRET_KEY'] = 'chickenstuffe'
#     return web

web = Flask(__name__)
web.config['SECRET_KEY'] = 'chickenstuffe'
web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chicken.db' # create database
web.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

    def __repr__(self):
        return f'<User: {self.email}>'
        

# Define a function to create tables
def create_tables():
    with web.app_context():
        db.create_all()

if __name__ == "__main__":
    # Call the function to create tables
    create_tables()
    # Run the Flask app
    web.run(debug=True)


# new_user = User(user_id=122, name='John Doe', email='john@example.com', date_posted=datetime.now)
# db.session.add(new_user)
# db.session.commit()
# db.session.close()