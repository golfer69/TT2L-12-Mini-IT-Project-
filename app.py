from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os 


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_DIRECTORY'] = 'uploads/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app=create_app()

db = SQLAlchemy(app)

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.now)
    image_filename = db.Column(db.String(255))


@app.route('/', methods=['GET'])
def index():
    pics = os.listdir(app.config['UPLOAD_DIRECTORY'])
    texts = Text.query.all()
    return render_template('index.html', texts=texts, pics=pics)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if request.method == 'POST':
        content = request.form['content'] # get text from html form
        file = request.files['file']  # Access the uploaded file
        text = Text(content=content)
        db.session.add(text)
        db.session.commit()
    
        if file:

            filename = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                secure_filename(file.filename)
            ))

            text.image_filename = filename
            db.session.add(text)
            db.session.commit()
        
    return redirect('/')

@app.route('/serve-files/<filename>', methods=['GET'])
def serve_files(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
  post = Text.query.get(post_id)
  if post:
    # Delete the post object from the database
    db.session.delete(post)
    db.session.commit()
  return redirect('/')


if  __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    





