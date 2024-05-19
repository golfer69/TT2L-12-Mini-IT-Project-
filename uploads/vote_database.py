from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vote.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app=create_app()

db = SQLAlchemy(app)

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

    @property
    def vote_count(self):
        upvotes = Vote.query.filter_by(post_id=self.id, vote_type=True).count()
        downvotes = Vote.query.filter_by(post_id=self.id, vote_type=False).count()
        return upvotes - downvotes

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
#Run 
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('vote.html', posts=posts)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Assume user is logged in and user_id is 1 for this example
    user = User.query.get(1)
    return render_template('vote.html', post=post, user=user)

@app.route('/posts/<int:post_id>/upvote', methods=['POST'])
def upvote_post(post_id):
    user_id = request.form.get('user_id')
    post = Post.query.get_or_404(post_id)
    vote = Vote.query.filter_by(user_id=user_id, post_id=post_id).first()
    
    if vote:
        return redirect(url_for('show_post', post_id=post_id))

    new_vote = Vote(user_id=user_id, post_id=post_id, vote_type=True)
    db.session.add(new_vote)
    db.session.commit()
    return redirect(url_for('show_post', post_id=post_id))

@app.route('/posts/<int:post_id>/downvote', methods=['POST'])
def downvote_post(post_id):
    user_id = request.form.get('user_id')
    post = Post.query.get_or_404(post_id)
    vote = Vote.query.filter_by(user_id=user_id, post_id=post_id).first()
    
    if vote:
        return redirect(url_for('show_post', post_id=post_id))

    new_vote = Vote(user_id=user_id, post_id=post_id, vote_type=False)
    db.session.add(new_vote)
    db.session.commit()
    return redirect(url_for('show_post', post_id=post_id))

if __name__ == '__main__':
    app.run(debug=True)
