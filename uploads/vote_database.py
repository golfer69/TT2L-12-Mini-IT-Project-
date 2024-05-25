from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def create_app():
   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///votes.db'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   return app

app=create_app()
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    votes = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.now)

# Create or migrate database
db.create_all()

# Define routes and other functionality here...
@app.route('/vote', methods=['POST'])
def vote():
    data = request.json  # Assuming JSON data is sent
    post_id = data['post_id']
    vote_type = data['vote_type']
    
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    if vote_type == 'upvote':
        post.votes += 1
    elif vote_type == 'downvote':
        post.votes -= 1

    db.session.commit()
    return jsonify({'votes': post.votes})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
