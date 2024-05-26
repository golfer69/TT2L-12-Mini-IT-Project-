from flask import Flask, request, render_template, redirect, url_for
import re
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tag_user.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app=create_app()
    
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='comments')
    date_added = db.Column(db.DateTime, default=datetime.now)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.relationship('Comment', back_populates='tags')
    user = db.relationship('User')
    date_added = db.Column(db.DateTime, default=datetime.now)

User.comments = db.relationship('Comment', back_populates='user')
Comment.tags = db.relationship('Tag', back_populates='comment')

def parse_tags(comment_content):
    pattern = r'@(\w+)'  # Find the username starts with @
    usernames = re.findall(pattern, comment_content)
    return usernames

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    user_id = request.form['user_id']
    content = request.form['content']
    
    # Create comments
    comment = Comment(content=content, user_id=user_id)
    db.session.add(comment)
    db.session.commit()
    
    # Parse and save tags
    tagged_usernames = parse_tags(content)
    for username in tagged_usernames:
        tagged_user = User.query.filter_by(username=username).first()
        if tagged_user:
            tag = Tag(comment_id=comment.id, user_id=tagged_user.id)
            db.session.add(tag)
    
    db.session.commit()
    return redirect(url_for('tag_user'))

@app.route('/')
def tag_user():
    comments = Comment.query.all()
    return render_template('tag_user.html', comments=comments)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)