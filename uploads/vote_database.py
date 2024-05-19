from flask import Flask, render_template, request, redirect, url_for 
# import sqlite3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comment.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app=create_app()

db = SQLAlchemy(app)

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    message_content = db.Column(db.String(255))
    vote_type = db.Column(db.String(10), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now)

# Route for HTML file
@app.route("/", methods=["GET", "POST"])
def user_comment():
    if request.method == 'POST':
        username = request.form["username"]
        message_content = request.form["message_content"]
        vote_type = request.form["vote_type"]
        text = Text(username=username, message_content=message_content, vote_type=vote_type)
        
        db.session.add(text)
        db.session.commit()
        return redirect(url_for('user_comment'))
    else:
        texts = Text.query.all()
        return render_template('comment.html', texts=texts)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
