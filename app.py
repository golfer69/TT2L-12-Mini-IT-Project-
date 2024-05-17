from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash
from werkzeug.utils import secure_filename
import os 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_bcrypt import Bcrypt
from itsdangerous import TimedSerializer
from flask_mail import Mail, Message
from sqlalchemy.orm import relationship 
from sqlalchemy import ForeignKey





def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='chickenstuffe'
    app.config['UPLOAD_DIRECTORY'] = 'uploads/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS']=True
    # app.config['MAIL_USERNAME'] = os.environment.get('EMAIL_USER')
    # app.config['MAIL_PASSWORD'] = os.environment.get('EMAIL_PASS')
    return app

app=create_app()
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
# mail=Mail(app)


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(150), nullable=False, unique=True)
    password= db.Column(db.String(40), nullable=False)
    email= db.Column(db.String(200), nullable=False, unique=True)
    posts= db.Relationship('Post', backref=db.backref('poster'))

    def get_reset_token(self, expire_sec=1800):
        seconds = TimedSerializer(app.config['SECRET_KEY'], expire_sec)
        return seconds.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        seconds = TimedSerializer(app.config['SECRET_KEY'])
        try:
            user_id=seconds.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)



class Post(db.Model):
    __tablename__ = '_post_'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.now)
    image_filename = db.Column(db.String(255))
    id_for_comments = db.relationship('Comment', backref='text', lazy=True)
    

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # Foreign key referencing Text.id
    comment_content = db.Column(db.Text)


# create database
with app.app_context():
    # Create Text table first
    db.create_all()

class RegisterForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Username'})
    password= PasswordField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Password'})
    password= EmailField(validators=[InputRequired(), Length(min=40, max=100)], render_kw={'placeholder':'Email'})
    submit= SubmitField('Register')

    def validate_username(self, username):
        existing_username=User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError('That username already exists. Please choose another one')

    def validate_username(self, email):
        existing_email=User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('That email already exists. Please choose another one')


class LoginForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Username'})
    password= PasswordField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Password'})
    submit= SubmitField('Login')

# class RequestResetForm(FlaskForm):
#     password= PasswordField(validators=[DataRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Password'})
#     submit= SubmitField('Request Password Reset')
#     def validate_username(self, username):
#         existing_username=User.query.filter_by(username=username.data).first()
#         if existing_username is None:
#             raise ValidationError('There is no account with that username. You must register first.')


# class ResetPasswordForm(FlaskForm):
#     password=PasswordField('Password', validators=[DataRequired()])
#     confirm_password=PasswordField('Confirm Password', validators=[DataRequired()])
#     submit= SubmitField('Reset Password')


@app.route('/', methods=['GET'])
def index():
    pics = os.listdir(app.config['UPLOAD_DIRECTORY'])
    texts = Post.query.all()
    return render_template('index.html', texts=texts, pics=pics)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content'] # get text from html form
        file = request.files['file']  # Access the uploaded file
        text = Post(title=title, content=content)
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

@app.route('/create', methods=['GET'])
def create():
    pics = os.listdir(app.config['UPLOAD_DIRECTORY'])
    texts = Post.query.all()
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
  post = Post.query.get(post_id)
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

# @app.route('/post/<int:post_id>', methods=['GET','POST'])
# def show_post(post_id):
#     post = Post.query.get(post_id)
#     comments = Comment.query.all()
    

#     if request.method == 'POST':
#         username = request.form["username"] # account will handle this part
#         comment_content = request.form["comment_content"]

#         comment = Comment(username=username, comment_content=comment_content)
        
#         db.session.add(comment)
#         db.session.commit()
#         return redirect(url_for('show_post'), comments=comments)

#     if not post:
#         return redirect('/')  # Handle non-existent post
        
#     return render_template('post.html',post=post, comments=comments)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()  # Filter comments by post ID

    if request.method == 'POST':
        username = request.form["username"]
        comment_content = request.form["comment-content"]
        post_id = request.form["post_id"]  # Access post ID from the hidden field

        # Validate user input (optional)
        # if not username or not comment_content:
        #     # Handle invalid input (e.g., display error message)
        #     pass

        comment = Comment(username=username, comment_content=comment_content, post_id=post_id)
        db.session.add(comment)
        db.session.commit()

        # Redirect back to the updated post page using the correct post ID
        return redirect(url_for('show_post', post_id=post_id))  # Include post_id in redirect

    if not post:
        return redirect('/')  # Handle non-existent post

    return render_template('post.html', post=post, comments=comments)


# def send_reset_email(user):
#     token= user.get_reset_token()
#     msg=Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
#     msg.body=f'''To reset your password, visit the following link:
# {url_for('reset_token', token=token, _external=True)} 

# If you did not make this request, then ignore this email   
# '''
#     mail.send(msg)


# @app.route('/reset_password', methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form=RequestResetForm()
#     if form.validate_on_submit():
#         user=user.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent to reset your password')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)



# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     new_user=new_user.verify_reset_token(token)
#     if new_user is None:
#         flash("that is an invalid or expired token", 'warning')
#         return redirect(url_for('reset_request'))
#     form= ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')        
#         new_user.password= hashed_password
#         db.session.commit()
#         flash('Your password has been updated!')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html', title='Reset Password', form=form)


if  __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

