from flask import Flask, render_template, request, redirect, url_for 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vote.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app=create_app()

db = SQLAlchemy(app)

from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    vote_type = db.Column(db.Boolean, nullable=False)  # True for upvote, False for downvote
    date_added = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref=db.backref('votes', lazy=True))
    post = db.relationship('Post', backref=db.backref('votes', lazy=True))

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_vote'),)

# Create users
user1 = User(username='user1', email='user1@example.com', password_hash='hashed_password_1')
user2 = User(username='user2', email='user2@example.com', password_hash='hashed_password_2')

db.session.add(user1)
db.session.add(user2)
db.session.commit()

# Create posts
post1 = Post(title='First Post', content='This is the content of the first post', user_id=user1.id)
post2 = Post(title='Second Post', content='This is the content of the second post', user_id=user2.id)

db.session.add(post1)
db.session.add(post2)
db.session.commit()

# Create votes
vote1 = Vote(user_id=user1.id, post_id=post1.id, vote_type=True)  # user1 upvotes First Post
vote2 = Vote(user_id=user2.id, post_id=post1.id, vote_type=False) # user2 downvotes First Post
vote3 = Vote(user_id=user1.id, post_id=post2.id, vote_type=True)  # user1 upvotes Second Post

db.session.add(vote1)
db.session.add(vote2)
db.session.add(vote3)
db.session.commit()

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return render_template([post.title for post in posts])

@app.route('/posts/<int:post_id>/upvote', methods=['POST'])
def upvote_post(post_id):
    user_id = request.method.get('user_id')
    post = Post.query.get_or_404(post_id)
    vote = Vote.query.filter_by(user_id=user_id, post_id=post_id).first()
    
    if vote:
        return render_template({'message': 'User has already voted on this post'}), 400

    new_vote = Vote(user_id=user_id, post_id=post_id, vote_type=True)
    db.session.add(new_vote)
    db.session.commit()
    return redirect(url_for('upvote_post(post_id)'))

@app.route('/posts/<int:post_id>/downvote', methods=['POST'])
def downvote_post(post_id):
    user_id = request.method.get('user_id')
    post = Post.query.get_or_404(post_id)
    vote = Vote.query.filter_by(user_id=user_id, post_id=post_id).first()
    
    if vote:
        return render_template({'message': 'User has already voted on this post'}), 400

    new_vote = Vote(user_id=user_id, post_id=post_id, vote_type=False)
    db.session.add(new_vote)
    db.session.commit()
    return redirect(url_for('downvote_post(post_id)'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)