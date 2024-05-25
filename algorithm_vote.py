from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///algorithm_vote.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('algorithm_vote.html', posts=posts)

@app.route('/upvote/<int:post_id>', methods=['POST'])
def upvote(post_id):
    post = Post.query.get_or_404(post_id)
    post.upvotes += 1
    db.session.commit()
    return jsonify({"success": True, "upvotes": post.upvotes})

@app.route('/downvote/<int:post_id>', methods=['POST'])
def downvote(post_id):
    post = Post.query.get_or_404(post_id)
    post.downvotes += 1
    db.session.commit()
    return jsonify({"success": True, "downvotes": post.downvotes})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
