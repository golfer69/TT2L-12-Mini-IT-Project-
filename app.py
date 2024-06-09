from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, EmailField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import uuid as uuid
from flask_migrate import Migrate
from sqlalchemy import desc
from apscheduler.schedulers.background import BackgroundScheduler


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='chickenstuffe'
    app.config['UPLOAD_DIRECTORY'] = 'uploads/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app=create_app()
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
migrate = Migrate(app,db)

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
    updates= db.relationship('Update', backref='poster', lazy=True)
    date_joined= db.Column(db.DateTime, default=datetime.now)

    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.now)
    image_filename = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    anonymous  = db.Column(db.Integer)
    votes = db.Column(db.Integer, default=0)
    hidden_votes = db.Column(db.Integer, default=0) # for algorithms
    id_for_comments = db.relationship('Comment', backref='text', lazy=True)

    def get_hot_filter(self):
        # """
        # Returns a filter for posts ordered by hidden_votes (descending)
        # """
        return Post.query.order_by(desc(Post.hidden_votes))

    def get_new_filter(self):
        # """
        # Returns a filter for posts ordered by date_added (descending)
        # """
        return Post.query.order_by(desc(Post.date_added))

    def get_top_filter(self):
        # """
        # Returns a filter for posts ordered by votes (descending)
        # """
        return Post.query.order_by(desc(Post.votes))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # Foreign key referencing Text.id
    comment_content = db.Column(db.Text)
    votes = db.Column(db.Integer, default=0)
    anonymous  = db.Column(db.Integer)

class Community(db.Model):
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    about = db.Column(db.String(255))
    community = db.relationship('Post', backref='community', lazy=True)

class Votes(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    vote_type = db.Column(db.Integer)

class Update(db.Model):
    __tablename__ = 'update'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    about = db.Column(db.String(1000), nullable=True)
    location = db.Column(db.String(1000), nullable=True)
    interests = db.Column(db.String(1000), nullable=True)
    faculty = db.Column(db.String(1000), nullable=True)
    profile_pic= db.Column(db.String(10000), nullable=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

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


class EntryForm(FlaskForm):
    name= StringField(label='Name')
    age= StringField(label='Age', validators=[Length(max=3)])
    about= StringField(label='About', validators=[Length(min=7, max=1000)])
    location= StringField(label='Location', validators=[Length(min=1, max=100)])
    interests= StringField(label='Interests', validators=[Length(min=1, max=1000)])    
    faculty= StringField(label='Faculty', validators=[Length(min=1, max=100)])
    profile_pic=FileField(label='Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit= SubmitField('Submit')

@app.context_processor
def inject_user():
    if current_user.is_authenticated:
        update_user=Update.query.filter_by(user_id=current_user.id).first()
        return dict(update_user=update_user)
    return dict(update_user=None)

@app.route('/', methods=['GET'])
def index():
    pics = os.listdir(app.config['UPLOAD_DIRECTORY'])
    filter_option = request.args.get('filter_option')
    if filter_option:
        if filter_option == 'top':
            posts = Post.get_top_filter(Post) 
        elif filter_option == 'new':
            posts = Post.get_new_filter(Post)  # Using defined method
        else:
            posts = Post.get_hot_filter(Post)  #hot for default
    else:
        posts = Post.get_hot_filter(Post)
    communities = Community.query.all()
    profile_pic= None
    if current_user.is_authenticated:
        update_user=Update.query.filter_by(user_id=current_user.id).first()
        if update_user and update_user.profile_pic:
            profile_pic=url_for('static', filename='profile_pics/' + update_user.profile_pic)

        # Get all votes for the current user (assuming `current_user` is available)
        current_user_id = current_user.id
        user_votes = Votes.query.filter_by(user_id=current_user_id).all()
        
        # Convert user votes to a dictionary for faster lookups by post ID
        vote_dict = {vote.post_id: vote.vote_type for vote in user_votes}
    else:
        # Provide an empty dictionary as default for unauthenticated users
        vote_dict = {}
    return render_template('index.html', posts=posts, pics=pics, communities=communities , profile_pic=profile_pic, vote_dict=vote_dict,page_title="MMU Reddit | Main Page")

@app.route('/create', methods=['GET'])
@login_required
def create():
    communities = Community.query.all()
    update_user=Update.query.filter_by(user_id=current_user.id).first()
    profile_pic= None # this is not necessary
    if update_user and update_user.profile_pic:
        profile_pic=url_for('static', filename='profile_pics/' + update_user.profile_pic)
    return render_template('create.html', communities=communities, profile_pic=profile_pic, page_title="Create a post")

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
                anonymous = request.form.get('anonymous')  # Default to False for non-checked checkbox
                post = Post(title=title, content=content, poster_id=poster, community_id=community_id, anonymous=anonymous)
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
                anonymous = request.form.get('anonymous') 
                comment = Comment(poster_id=poster_id, comment_content=comment_content, post_id=post_id, anonymous=anonymous)
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
        return redirect(url_for('user_posts'))
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
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash("Invalid usename or password. Please try again")
            return render_template('login.html', form=form)
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password. Please try again")
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user_posts', methods=['GET', 'POST'])
@login_required
def user_posts():
    user_posts= Post.query.filter_by(poster_id=current_user.id).all()
        # Get all votes for the current user (assuming `current_user` is available)
    current_user_id = current_user.id
    user_votes = Votes.query.filter_by(user_id=current_user_id).all()
    
    # Convert user votes to a dictionary for faster lookups by post ID
    vote_dict = {vote.post_id: vote.vote_type for vote in user_votes}
    return render_template('user_posts.html', posts=user_posts, vote_dict=vote_dict,page_title="User Posts")

@app.route('/account', methods=['GET'])
@login_required
def account():
    user=current_user
    update_user = Update.query.filter_by(user_id=current_user.id).first()
    return render_template('account.html', user=user, update_user=update_user, page_title="User")


def save_profile_pic(profile_pic_file):
    if profile_pic_file:
        filename=secure_filename(profile_pic_file.filename)
        unique_id_filename=str(uuid.uuid1()) + '_' + filename
        upload_dir='static/profile_pics'
        os.makedirs(upload_dir, exist_ok=True)
        profile_pic_path=os.path.join(upload_dir, unique_id_filename)
        profile_pic_file.save(profile_pic_path)
        return unique_id_filename
    else:
        return None


@app.route('/user_details/<int:id>', methods=['GET', 'POST'])
@login_required
def user_details(id):
    form = EntryForm()
    update_user = Update.query.filter_by(user_id=id).first()

    if form.validate_on_submit():
        profile_pic_filename=save_profile_pic(form.profile_pic.data)
        if update_user:
            # Update existing user details
            update_user.name = form.name.data
            update_user.age = form.age.data
            update_user.about = form.about.data
            update_user.location = form.location.data
            update_user.interests = form.interests.data
            update_user.faculty = form.faculty.data
            if profile_pic_filename:
                update_user.profile_pic = profile_pic_filename
        else:
            # Create new user details
            update_user = Update(
                name=form.name.data,
                age=form.age.data,
                about=form.about.data,
                location=form.location.data,
                interests=form.interests.data,
                faculty=form.faculty.data,
                profile_pic=profile_pic_filename,
                user_id=id
            )
            db.session.add(update_user)
        
        try:
            db.session.commit()
            return redirect(url_for('account'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to update user details: {str(e)}', 'danger')

    # Prepopulate the form with existing data if available
    if update_user:
        form.name.data = update_user.name
        form.age.data = update_user.age
        form.about.data = update_user.about
        form.location.data = update_user.location
        form.interests.data = update_user.interests
        form.faculty.data = update_user.faculty


    return render_template('user_details.html', title='User Details', form=form)




@app.route('/admin')
@login_required
def admin():
    id= current_user.id
    if id==1 or id==6:
        return render_template('admin.html', page_title="Admin Page")
    
@app.route('/delete', methods=['POST'])
@login_required
def delete():
    item = request.form.get('item')
    if current_user.is_authenticated:
        if item == "post":
            post_id = request.form.get('post_id')
            post = Post.query.get(post_id)
            if post.poster_id == current_user.id:
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
        if item == "comment":
            comment_id = request.form.get('comment_id')
            post_id = request.form.get('post_id')
            comment = Comment.query.get(comment_id)
            if comment.poster_id == current_user.id:
                db.session.delete(comment)
                db.session.commit()
            return redirect(url_for('show_post', post_id=post_id))

@app.route('/edit/<int:post_id>', methods=['GET','POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    return render_template('edit.html',post=post)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    current_user_id = None  # Initialize to None
    post = Post.query.get(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()  # Filter comments by post ID
        # Get all votes for the current user (assuming `current_user` is available)
    if current_user.is_authenticated:
        current_user_id = current_user.id
    user_votes = Votes.query.filter_by(user_id=current_user_id).all()
    
    # Convert user votes to a dictionary for faster lookups by post ID
    vote_dict = {vote.post_id: vote.vote_type for vote in user_votes}
    vote_dict_comment = {vote.comment_id: vote.vote_type for vote in user_votes}

    if not post:
        return redirect('/')  # Handle non-existent post
    
    return render_template('post.html', post=post, comments=comments, page_title=post.title, vote_dict=vote_dict, vote_dict_comment=vote_dict_comment)

@app.route('/community/<string:community_name>', methods=['GET'])
def show_community(community_name):
    community = Community.query.filter_by(name=community_name).first()
    if community:
      community_id = community.id # Get the id of the community
    community = Community.query.get(community_id)
    community_posts = Post.query.filter_by(community_id=community_id)
    filter_option = request.args.get('filter_option')
    if filter_option:
        if filter_option == 'top':
            posts = Post.get_top_filter(Post) 
        elif filter_option == 'new':
            posts = Post.get_new_filter(Post)  # Using defined method
        else:
            posts = Post.get_hot_filter(Post)  # hot for default
    else:
        posts = Post.get_hot_filter(Post)
    # Get all votes for the current user (assuming `current_user` is available)
    current_user_id = None  # Initialize to None
    if current_user.is_authenticated:
        current_user_id = current_user.id
    user_votes = Votes.query.filter_by(user_id=current_user_id).all()
    
    # Convert user votes to a dictionary for faster lookups by post ID
    vote_dict = {vote.post_id: vote.vote_type for vote in user_votes}
    return render_template('community.html', posts=posts, community=community, page_title=community_name, vote_dict=vote_dict)

# def calculate_time_difference(posted_time):
#     # Your time difference calculation function here

#  @app.route('/post')
#  def post():
#     posted_time = datetime(2022, 1, 1, 12, 0, 0)  # Replace this with the actual posted time
#     time_since_posted = calculate_time_difference(posted_time)
#     return render_template('post.html', time_since_posted=time_since_posted)

# Upvotes and downvotes
@app.route('/upvote/<int:post_id>', methods=['POST'])
def upvote(post_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user_id = current_user.id
    post = Post.query.get(post_id)
    if post:
        existing_vote = Votes.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_vote and existing_vote.vote_type == "downvote":
            existing_vote.vote_type = "upvote"
        else:
            vote = Votes(user_id=user_id, post_id=post_id, vote_type="upvote")
            db.session.add(vote)
            
        # Count upvotes and downvotes separately
        upvote_count = Votes.query.filter_by(post_id=post_id, vote_type="upvote").count()
        downvote_count = Votes.query.filter_by(post_id=post_id, vote_type="downvote").count()

        post.votes = upvote_count - downvote_count
        db.session.commit()
        return jsonify({'message': 'Upvoted successfully', 'votes': post.votes})
    else:
        return jsonify({'error': 'Post not found'}), 404

@app.route('/downvote/<int:post_id>', methods=['POST'])
def downvote(post_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user_id = current_user.id
    post = Post.query.get(post_id)
    if post:
        existing_vote = Votes.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_vote and existing_vote.vote_type == "upvote":
            existing_vote.vote_type = "downvote"
        else:
            vote = Votes(user_id=user_id, post_id=post_id, vote_type="downvote")
            db.session.add(vote)

        # Count upvotes and downvotes separately
        upvote_count = Votes.query.filter_by(post_id=post_id, vote_type="upvote").count()
        downvote_count = Votes.query.filter_by(post_id=post_id, vote_type="downvote").count()

        post.votes = upvote_count - downvote_count
        db.session.commit()
        return jsonify({'message': 'Downvoted successfully', 'votes': post.votes})
    else:
        return jsonify({'error': 'Post not found'}), 404

@app.route('/unvote/<int:post_id>', methods=['POST'])
def unvote(post_id):
    user_id = current_user.id
    post = Post.query.get(post_id)
    if post:
        existing_vote = Votes.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_vote:
            db.session.delete(existing_vote)
            # Count upvotes and downvotes separately
            upvote_count = Votes.query.filter_by(post_id=post_id, vote_type="upvote").count()
            downvote_count = Votes.query.filter_by(post_id=post_id, vote_type="downvote").count()

            post.votes = upvote_count - downvote_count
            db.session.commit()
            return jsonify({'message': 'Vote removed successfully', 'votes': post.votes})
        else:
            return jsonify({'error': 'No vote found to remove'}), 404
    else:
        return jsonify({'error': 'Post not found'}), 404
    
@app.route('/check_vote/<int:post_id>/<vote_type>', methods=['GET'])
@login_required
def check_vote(post_id, vote_type):
    if current_user.is_authenticated:
        user_id = current_user.id
        vote_exists = Votes.query.filter_by(user_id=user_id, post_id=post_id, vote_type=vote_type).first()
        return jsonify({'voted': vote_exists is not None})

# Upvotes and downvotes FOR COMMENTS
@app.route('/voteComment/<int:comment_id>', methods=['POST'])
def voteComment(comment_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user_id = current_user.id
    vote_type = request.json.get('vote_type')
    if not vote_type:
        # Handle error if vote_type is missing
        return jsonify({'error': 'Missing vote type'}), 400 
    comment = Comment.query.get(comment_id)
    if comment:
        if vote_type == 'upvote':
            existing_vote = Votes.query.filter_by(user_id=user_id, comment_id=comment_id).first()
            if existing_vote and existing_vote.vote_type == "downvote": #check first
                existing_vote.vote_type = "upvote"
            else: # if not voted then add new vote
                vote = Votes(user_id=user_id, comment_id=comment_id, vote_type="upvote")
                db.session.add(vote)
                
            # Count upvotes and downvotes separately
            upvote_count = Votes.query.filter_by(comment_id=comment_id, vote_type="upvote").count()
            downvote_count = Votes.query.filter_by(comment_id=comment_id, vote_type="downvote").count()

            comment.votes = upvote_count - downvote_count
            db.session.commit()
            return jsonify({'message': 'Upvoted successfully', 'votes': comment.votes})
        if vote_type == "downvote":
            existing_vote = Votes.query.filter_by(user_id=user_id, comment_id=comment_id).first()
            if existing_vote and existing_vote.vote_type == "upvote":
                existing_vote.vote_type = "downvote"
            else:
                vote = Votes(user_id=user_id, comment_id=comment_id, vote_type="downvote")
                db.session.add(vote)
            # Count upvotes and downvotes separately
            upvote_count = Votes.query.filter_by(comment_id=comment_id, vote_type="upvote").count()
            downvote_count = Votes.query.filter_by(comment_id=comment_id, vote_type="downvote").count()

            comment.votes = upvote_count - downvote_count
            db.session.commit()
            return jsonify({'message': 'Downvoted successfully', 'votes': comment.votes})
    else:
        return jsonify({'error': 'Post not found'}), 404

@app.route('/unvoteComment/<int:comment_id>', methods=['POST'])
def unvoteComment(comment_id):
    user_id = current_user.id
    comment = Comment.query.get(comment_id)
    if comment:
        existing_vote = Votes.query.filter_by(user_id=user_id, comment_id=comment_id).first()
        if existing_vote:
            db.session.delete(existing_vote)
            # Count upvotes and downvotes separately
            upvote_count = Votes.query.filter_by(comment_id=comment_id, vote_type="upvote").count()
            downvote_count = Votes.query.filter_by(comment_id=comment_id, vote_type="downvote").count()

            comment.votes = upvote_count - downvote_count
            db.session.commit()
            return jsonify({'message': 'Vote removed successfully', 'votes': comment.votes})
        else:
            return jsonify({'error': 'No vote found to remove'}), 404
    else:
        return jsonify({'error': 'Post not found'}), 404
    
@app.route('/checkVoteComment/<int:comment_id>/<vote_type>', methods=['GET'])
@login_required
def checkVoteComment(comment_id, vote_type):
    if current_user.is_authenticated:
        user_id = current_user.id
        vote_exists = Votes.query.filter_by(user_id=user_id, comment_id=comment_id, vote_type=vote_type).first()
        return jsonify({'voted': vote_exists is not None})


@app.route('/filter_posts', methods=['POST'])
def filter_posts():
  filter_option = request.form.get('filter_option')
  redirect_to = request.form.get('redirect_to')
  community_name = request.form.get('community_name')

  if redirect_to == 'index':
    return redirect(url_for('index', filter_option=filter_option))
  if redirect_to == 'community':
    return redirect(url_for('show_community', filter_option=filter_option, community_name=community_name))

# decay function
def decay_hidden_votes(post):
    current_time = datetime.now()

    if post.hidden_votes is None:
        post.hidden_votes = post.votes 
    else:
        post.hidden_votes

    post_age_days = (current_time - post.date_added).days
    post_title = post.title
    decay_factor = 0.99  # Votes decay by 1% each day
    decayed_hidden_votes = post.hidden_votes * (decay_factor ** post_age_days) #decay more and more by days go by

    # Ensure the decayed value doesn't go below 0
    decayed_hidden_votes = max(decayed_hidden_votes, 0)

    return int(decayed_hidden_votes)

# to decay
def decay_all_hidden_votes():
    posts = Post.query.all()

    for post in posts:
        decayed_votes = decay_hidden_votes(post)
        post.hidden_votes = decayed_votes

    db.session.commit()

#decaying the votes
def schedule_decay():
    with app.app_context():
        decay_all_hidden_votes()

# Create a scheduler instance
scheduler = BackgroundScheduler()
scheduler.add_job(schedule_decay, 'interval', days=1)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)

# def calculate_time_difference(posted_time):
#     current_time = datetime.now()
#     time_difference = current_time - posted_time

#     seconds = time_difference.total_seconds()
#     minutes = seconds / 60
#     hours = minutes / 60
#     days = hours / 24
#     weeks = days / 7
#     months = days / 30
#     years = days / 365

    #     if seconds < 60:
#         return f"{int(seconds)} seconds ago"
#     elif minutes < 60:
#         return f"{int(minutes)} minutes ago"
#     elif hours < 24:
#         return f"{int(hours)} hours ago"
#     elif days < 7:
#         return f"{int(days)} days ago"
#     elif weeks < 4:
#         return f"{int(weeks)} weeks ago"
#     elif months < 12:
#         return f"{int(months)} months ago"
#     else:
#         return f"{int(years)} years ago"
    
# #how far back was a post posted

# def calculate_time_difference(posted_time):
#     current_time = datetime.now()
#     time_difference = current_time - posted_time

#     seconds = time_difference.total_seconds()
#     minutes = seconds / 60
#     hours = minutes / 60
#     days = hours / 24
#     weeks = days / 7
#     months = days / 30
#     years = days / 365

#     if seconds < 60:
#         return f"{int(seconds)} seconds ago"
#     elif minutes < 60:
#         return f"{int(minutes)} minutes ago"
#     elif hours < 24:
#         return f"{int(hours)} hours ago"
#     elif days < 7:
#         return f"{int(days)} days ago"
#     elif weeks < 4:
#         return f"{int(weeks)} weeks ago"
#     elif months < 12:
#         return f"{int(months)} months ago"
#     else:
#         return f"{int(years)} years ago"

# # Example usage
# posted_time = datetime(2022, 1, 1, 12, 0, 0)  # Replace this with the actual posted time
# time_since_posted = calculate_time_difference(posted_time)
# print(time_since_posted)
