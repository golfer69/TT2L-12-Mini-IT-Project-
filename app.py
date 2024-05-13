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
    app.config['SECRET_KEY']='chickenstuffe'
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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(150), nullable=False, unique=True)
    password= db.Column(db.String(40), nullable=False)

class Text(db.Model):
    __bind_key__ = 'data'  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.now)
    image_filename = db.Column(db.String(255))

<<<<<<< HEAD
#user profile customization
#sqlalchemy

app.config['SQLALCHEMY_DATABASE_URI']='sqlite;/// profiles.db'

#secret key 
app.config['SECRET_KEY']='secret user profile'
#initialize  the database

db=SQLAlchemy
#Upload picture feature

class Users(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(10),nullable=False)
    location=db.Column(db.String(20),nullable=False)
    date_added= db.Column(db.DateTime,default=datetime.now)

    #Create a string

    def __repr__(self):
        return '<Username%>' % self.name
    

    class Userform(FlaskForm):
        username=StringField()

UPLOAD_FOLDER='profile_uploads'
allowed_extensions={'png','jpg','jpeg','gif'}

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def allowed_file(filename):
    return filename.lower().endswith(('.png','.jpg','.jpeg','.gif'))

@app.route('/')
def index():
    return render_template('profile.html')

@app.route('/upload_profile',methods=['GET','POST'])
def profile():
    if request.method=='POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file=request.files['file']

        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
          

        else:
            return redirect(request.url)

# Create comment database
# sqlalchemy 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite;/// comment.db'

db= SQLAlchemy(app)

class Text(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(255))
     message_content = db.Column(db.String(255))
     date_added = db.Column(db.DateTime, default=datetime.now)

@app.route('/comment', methods=['GET', 'POST'])
def user_comment():
    if request.method == 'POST':
        username = request.form["username"]
        message_content = request.form["message_content"]
        text = Text(username=username, message_content=message_content)
        
        db.session.add(text)
        db.session.commit()
        return redirect(url_for('user_comment'))
    else:
        texts = Text.query.all()
        return render_template('comment.html', texts=texts)

# Create user table 
def create_user_table():

    class Text(db.Model):
     __bind_key__ = 'data'  
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(255))
bio = db.Column(db.String(50))
image_filename = db.Column(db.String(255))

# Add user to database 


# Route for HTML file 
@app.route("/", methods=["GET", "POST"])
def user_profile():
    if request.method == "POST":
     username = request.form["username"]
     bio = request.form["bio"]
       
        # Redirect to user profile page
    return redirect(url_for("thank_you"))

    # render profile.html
    return render_template("profile.html")


@app.route("/thank-you")
def thank_you():
    return "Your profile is successfully saved !"




=======
>>>>>>> main
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

@app.route('/', methods=['GET', 'POST'])
#user profile customization
#sqlalchemy

app.config['SQLALCHEMY_DATABASE_URI']='sqlite;/// profiles.db'

#secret key 
app.config['SECRET_KEY']='secret user profile'
#initialize  the database

db=SQLAlchemy
#Upload picture feature

class Users(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(10),nullable=False)
    location=db.Column(db.String(20),nullable=False)
    date_added= db.Column(db.DateTime,default=datetime.now)

    #Create a string

    def __repr__(self):
        return '<Username%>' % self.name
    

    class Userform(FlaskForm):
        username=StringField()

UPLOAD_FOLDER='profile_uploads'
allowed_extensions={'png','jpg','jpeg','gif'}

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def allowed_file(filename):
    return filename.lower().endswith(('.png','.jpg','.jpeg','.gif'))

@app.route('/')
def index():
    return render_template('profile.html')

@app.route('/upload_profile',methods=['GET','POST'])
def profile():
    if request.method=='POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file=request.files['file']

        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
          

        else:
            return redirect(request.url)


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
    files = os.listdir(app.config['UPLOAD_DIRECTORY'])
    if request.method == 'POST':
        content = request.form['content']
        text = Text(content=content)
        db.session.add(text)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        texts = Text.query.all()
        return render_template('index.html', texts=texts, files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
<<<<<<< HEAD
=======
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content'] # get text from html form
        file = request.files['file']  # Access the uploaded file
        text = Text(title=title, content=content)
        db.session.add(text)
        db.session.commit()
>>>>>>> main
    
    if file:
        file.save(os.path.join(
            app.config['UPLOAD_DIRECTORY'],
            secure_filename(file.filename)
        ))
    
    return redirect('/')

@app.route('/create', methods=['GET'])
def create():
    pics = os.listdir(app.config['UPLOAD_DIRECTORY'])
    texts = Text.query.all()
    return render_template('create.html', texts=texts, pics=pics)


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

<<<<<<< HEAD

if  __name__ == '__main__':
     with app.app_context():
        db.create_all()
=======
if  __name__ == '__main__':
>>>>>>> main
    app.run(debug=True)