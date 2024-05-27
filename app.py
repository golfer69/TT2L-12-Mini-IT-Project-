from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash
from werkzeug.utils import secure_filename
import os 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='chickenstuffe'
    app.config['UPLOAD_DIRECTORY'] = 'uploads/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=465
    app.config['MAIL_USE_TLS']=False
    app.config['MAIL_USE_SSL']=True
    app.config['MAIL_USERNAME'] = 'halimalif13@gmail.com'
    app.config['MAIL_PASSWORD'] = 'alifakmalbinabdulhalim'
    return app

app=create_app()
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
mail=Mail(app)
serializer=URLSafeTimedSerializer(app.config['SECRET_KEY'])

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
    email= db.Column(db.String(80), nullable=False, unique=True)
    posts= db.relationship('Post', backref='poster', lazy=True)
    comments= db.relationship('Comment', backref='poster', lazy=True)
    updates= db.relationship('Update', backref='updating', lazy=True)
    date_joined= db.Column(db.DateTime, default=datetime.now)

    def get_token(self):
        return serializer.dumps({'user_id':self.id}, salt='password-reset-salt')
                                
    @staticmethod
    def verify_token(token):
        try:
            user_id = serializer.loads(token, salt='password-reset-salt', max_age=300)['user_id']
        except:
            SignatureExpired()
        return User.query.get(user_id)
    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.now)
    image_filename = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    id_for_comments = db.relationship('Comment', backref='text', lazy=True)
    
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # Foreign key referencing Text.id
    comment_content = db.Column(db.Text)

class Community(db.Model):
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    about = db.Column(db.String(255))
    community = db.relationship('Post', backref='community', lazy=True)

class Update(db.Model):
    __tablename__ = 'update'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    about = db.Column(db.String(1000))
    location = db.Column(db.String(1000))
    interests = db.Column(db.String(1000))
    faculty = db.Column(db.String(1000))
    updating_id=db.Column(db.Integer, db.ForeignKey('user.id'))





# create database
with app.app_context():
    # Create Text table first
    db.create_all()

class RegisterForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Username'})
    password= PasswordField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Password'})
    email= EmailField(validators=[InputRequired(), Length(min=10, max=100)], render_kw={'placeholder':'Email'})
    submit= SubmitField('Register')

    def validate_username(self, username):
        existing_username=User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError('That username already exists. Please choose another one')

    def validate_email(self, email):
        existing_email=User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('That email already exists. Please choose another one')


class LoginForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Username'})
    password= PasswordField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Password'})
    submit= SubmitField('Login')


class ResetRequestForm(FlaskForm):
    email= StringField(label='Email', validators=[InputRequired()])
    submit= SubmitField(label='Reset Password', validators=[InputRequired()])


class ResetPasswordForm(FlaskForm):
    password= PasswordField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Password'})
    confirm_password= PasswordField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={'placeholder':'Confirm Password'})
    submit= SubmitField('Change Password')

    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords do not match!')


class EntryForm(FlaskForm):
    name= StringField(label='Name')
    age= StringField(label='Age', validators=[Length(max=3)])
    about= StringField(label='About', validators=[Length(min=7, max=1000)])
    location= StringField(label='Location', validators=[Length(min=1, max=100)])
    interests= StringField(label='Interests', validators=[Length(min=1, max=1000)])    
    faculty= StringField(label='Faculty', validators=[Length(min=1, max=100)])
    submit= SubmitField('Submit')


@app.route('/', methods=['GET'])
def index():
    pics = os.listdir(app.config['UPLOAD_DIRECTORY'])
    posts = Post.query.all()
    return render_template('index.html', posts=posts, pics=pics, page_title="MMU Reddit | Main Page")

@app.route('/create', methods=['GET'])
@login_required
def create():
    pics = os.listdir(app.config['UPLOAD_DIRECTORY'])
    texts = Post.query.all()
    communities = Community.query.all()
    return render_template('create.html', texts=texts, pics=pics,communities=communities, page_title="Create a post")

@app.route('/createcommunity', methods=['GET'])
@login_required
def createcomm():
    return render_template('createcomm.html', page_title="Create community")

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    item = request.form.get('item')
    if current_user.is_authenticated:
        if request.method == 'POST':
            if item == "post":
                title = request.form['title']
                content = request.form['content'] # get text from html form
                file = request.files['file']  # Access the uploaded file
                poster= current_user.id
                community_id = request.form['community_id']
                post = Post(title=title, content=content, poster_id=poster, community_id=community_id)
                db.session.add(post)
                db.session.commit()
            
                if file:

                    filename = secure_filename(file.filename)
                    file.save(os.path.join(
                        app.config['UPLOAD_DIRECTORY'],
                        secure_filename(file.filename)
                    ))

                    post.image_filename = filename
                    db.session.add(post)
                    db.session.commit()

            if item == "community":
                name = request.form.get('name')
                about = request.form.get('about')
                community = Community(name=name, about=about)
                db.session.add(community)
                db.session.commit()

            if item == "comment":
                poster_id= current_user.id
                comment_content = request.form["comment-content"]
                post_id = request.form["post_id"]  # Access post ID from the hidden field

                comment = Comment(poster_id=poster_id, comment_content=comment_content, post_id=post_id)
                db.session.add(comment)
                db.session.commit()

                # Redirect back to the updated post page using the correct post ID
                return redirect(url_for('show_post', post_id=post_id))  # Include post_id in redirect
            
    return redirect('/')

@app.route('/update', methods=['GET','POST'])
def update():
    post_id = request.form['post_id'] 
    post = Post.query.get(post_id)
    if request.method == 'POST' and post.poster_id == current_user.id:
        
        new_title = request.form['title']
        new_content = request.form['content']

        post.title = new_title
        post.content = new_content
        
        db.session.commit()
    return redirect(url_for('show_post', post_id=post_id))

@app.route('/uploads/<path:filename>')
def serve_files(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')        
        new_user= User(email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash("Invalid usename or password. Please try again")
            return render_template('login.html', form=form)
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password. Please try again")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def send_mail(user):
    token=user.get_token()
    msg=Message('Password Reset Request', recipients=[user.email], sender='noreply@demo.com')
    msg.body=f''' To reset your password, please follow the link: {url_for(reset_token, token=token, _external=True)} If you didn't send a password request, please ignore this email'''
    Mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form=ResetRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
            return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user=User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token, please try again', 'warning')
        return redirect(url_for('reset_request'))
    
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')        
        db.session.add(hashed_password)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('change_password.html', title="Change Password", form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user_posts= Post.query.filter_by(poster_id=current_user.id).all()
    update=Update.query.filter_by(name=current_user.username).first()
    return render_template('dashboard.html', posts=user_posts, update=update, page_title="Dashboard")
    
# @app.route('/user_details', methods=['GET', 'POST'])
# @login_required
# def user_details():
#     update=Update.query.filter_by(name=current_user.username).first()
#     return render_template('user_details.html', update=update, page_title="User Details")


@app.route('/update_user_details', methods=['GET', 'POST'])
@login_required
def update_user_details(id):
    form=EntryForm()
    current_update=Update.query.filter_by(name=current_user.username).first()
    if form.validate_on_submit():
        if current_update:
            current_update.name=form.name.data
            current_update.age=form.age.data
            current_update.location=form.location.data
            current_update.about=form.about.data
            current_update.interests=form.interests.data
            current_update.faculty=form.faculty.data
        else:
            current_update=Update(name=form.name.data, 
                                    age=form.age.data,
                                    about=form.about.data,
                                    location=form.location.data,
                                    interests=form.interests.data,
                                    faculty=form.faculty.data)
            db.session.add(current_update)

        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('update_user_details.html',title='Update User Details', form=form)


@app.route('/admin')
@login_required
def admin():
    id= current_user.id
    if id==1 or id==6:
        return render_template('admin.html', page_title="Admin Page")
    
@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
  post = Post.query.get(post_id)
  poster=current_user.id
  if post.poster_id==poster:
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

@app.route('/edit/<int:post_id>', methods=['GET','POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    return render_template('edit.html',post=post)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()  # Filter comments by post ID

    if not post:
        return redirect('/')  # Handle non-existent post
    
    return render_template('post.html', post=post, comments=comments, page_title=post.title)

@app.route('/community/<string:community_name>', methods=['GET'])
def show_community(community_name):
    community = Community.query.filter_by(name=community_name).first()
    if community:
      community_id = community.id # Get the id of the community
    community = Community.query.get(community_id)
    community_posts = Post.query.filter_by(community_id=community_id)
    return render_template('community.html', posts=community_posts, community=community, page_title=community_name)






if  __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

def calculate_time_difference(posted_time):
    # Your time difference calculation function here

 @app.route('/post')
 def post():
    posted_time = datetime(2022, 1, 1, 12, 0, 0)  # Replace this with the actual posted time
    time_since_posted = calculate_time_difference(posted_time)
    return render_template('post.html', time_since_posted=time_since_posted)



#how far back was a post posted

def calculate_time_difference(posted_time):
    current_time = datetime.now()
    time_difference = current_time - posted_time

    seconds = time_difference.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    weeks = days / 7
    months = days / 30
    years = days / 365

    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif minutes < 60:
        return f"{int(minutes)} minutes ago"
    elif hours < 24:
        return f"{int(hours)} hours ago"
    elif days < 7:
        return f"{int(days)} days ago"
    elif weeks < 4:
        return f"{int(weeks)} weeks ago"
    elif months < 12:
        return f"{int(months)} months ago"
    else:
        return f"{int(years)} years ago"

# Example usage
posted_time = datetime(2022, 1, 1, 12, 0, 0)  # Replace this with the actual posted time
time_since_posted = calculate_time_difference(posted_time)
print(time_since_posted)








if  __name__ == '__main__':
    app.run(debug=True)