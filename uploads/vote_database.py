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

class Comment_Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    message_content = db.Column(db.String(255))
    vote = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default= datetime.now)

# Route
@app.route("/vote", methods=["GET","POST"])
def vote_action():
    if request.method == 'POST':
        username = request.form["username"]
        message_content = request.form["message_content"]
        vote = request.form["vote"]
        date_added = request.form["message_content"]
        cl = Comment_Like(username=username, message_content=message_content, vote=vote, date_added=date_added)
        
        db.session.add(cl)
        db.session.commit()
        return redirect(url_for('user_vote'))
    else:
        cl = Comment_Like.query.filter_by(id=1).first()
        cl.vote.count()
        return render_template('vote.html', cl=cl)

if  __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)