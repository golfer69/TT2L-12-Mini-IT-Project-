from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash
from werkzeug.utils import secure_filename
import os 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt




def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_DIRECTORY'] = 'uploads/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    app.config['SQLALCHEMY_BINDS'] = {'data': 'sqlite:///data.db'}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app=create_app()

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Text(db.Model):
    __bind_key__ = 'data'  
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.now)
    image_filename = db.Column(db.String(255))

with app.app_context():
    db.create_all()

class RegisterForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Username'})
    password= PasswordField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Password'})
    submit= SubmitField('Register')

    def validate_username(self, username):
        existing_username=User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError('That username already exists. Please choose another one')

class LoginForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Username'})
    password= PasswordField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Password'})
    submit= SubmitField('Login')

@app.route('/', methods=['GET'])
def index():
    pics = os.listdir(app.config['UPLOAD_DIRECTORY'])
    texts = Text.query.all()
    return render_template('index.html', texts=texts, pics=pics)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if request.method == 'POST':
        content = request.form['content'] # get text from html form
        file = request.files['file']  # Access the uploaded file
        text = Text(content=content)
        db.session.add(text)
        db.session.commit()
    
        if file:

            filename = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                secure_filename(file.filename)
            ))

            text.image_filename = filename
            db.session.add(text)
            db.session.commit()
        
    return redirect('/')

@app.route('/uploads/<path:filename>')
def serve_files(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')        
        new_user= User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'error')
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
@login_required
def admin():
    id= current_user.id
    if id==5 or id==6:
        return render_template('admin.html')
    else:
        flash("Only admins can access this page")
        return redirect(url_for('index'))
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
  post = Text.query.get(post_id)
  if post:
    # Delete the post object from the database
    db.session.delete(post)
    db.session.commit()
    
    # Delete the image file if it exists
    image_filename = post.image_filename
    if image_filename:
      image_path = os.path.join(app.config['UPLOAD_DIRECTORY'], image_filename)
      if os.path.exists(image_path):
        try:
          os.remove(image_path)
        except OSError as e:
          print(f"Error deleting image file: {e}")
          
  return redirect('/')

@app.route('/post/<int:post_id>', methods=['GET'])
def show_post(post_id):
    post = Text.query.get(post_id)
    if not post:
        return redirect('/')  # Handle non-existent post
    
    return render_template('post.html',post=post)  # Render a separate template for single post

if  __name__ == '__main__':
    app.run(debug=True)

