from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_DIRECTORY'] = 'uploads/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app=create_app()
db = SQLAlchemy(app) # Initialise database
bcrypt=Bcrypt(app)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password= db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class RegisterForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Username'})
    password= StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Password'})
    submit= SubmitField('Register')

def validate_username(self, username):
    existing_username=User.query.filter_by(username=username.data).first()
    if existing_username:
        raise ValidationError('That username already exists. Please choose another one')
# class Posts(db.Model):
#     posts_id=db.Column(db.Integer, primary_key=True)
#     image=db.Column(db.String(2000))
#     posts_title=db.Column(db.String(20000), nullable=False)
#     text=db.Column(db.String(20000), nullable=False)

def create_tables():
    with app.app_context().push():
        db.create_all()

app.app_context().push()

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_DIRECTORY'])
    return render_template('index.html', files=files)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashded_password= bcrypt.generate_password_hash(form.password.data)
        new_user= User(username=form.username.data, password=hashded_password)
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
    return render_template('register.html', form=form)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file'] 
    
    if file:
        file.save(os.path.join(
            app.config['UPLOAD_DIRECTORY'],
            secure_filename(file.filename)
        ))
    
    return redirect('/')

@app.route('/serve-files/<filename>', methods=['GET'])
def serve_files(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)

if  __name__ == '__main__':
    app.run(debug=True)
    





