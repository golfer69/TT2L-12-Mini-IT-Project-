from flask import Flask, render_template, request, jsonify
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///algorithm_vote.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app=create_app()

db = SQLAlchemy()
db.init_app(app)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    message_content = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    date_added= db.Column(db.DateTime, default=datetime.now)

class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    date_added= db.Column(db.DateTime, default=datetime.now)
    image_filename = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    id_for_comments = db.relationship('Comment', backref='post', lazy= True)

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('algorithm_vote.html', posts=posts)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    post_id = data.get('post_id')
    vote_type = data.get('vote_type')

    post = Post.query.get(post_id)

    if post:
        if vote_type == 'upvote':
            post.upvotes += 1
        elif vote_type == 'downvote':
            post.downvotes += 1
        db.session.commit()

        return jsonify({'success': True, 'post':{
            'id': post.id,
            'upvotes': post.upvotes,
            'downvotes': post.downvotes
        }})
    else:
        return jsonify({'success': False, 'error': 'Post not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
