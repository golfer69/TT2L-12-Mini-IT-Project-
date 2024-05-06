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


@app.route('/', methods=['GET', 'POST'])
def index():
    files = os.listdir(app.config['UPLOAD_DIRECTORY'])
    if request.method == 'POST':
        content = request.form['content']
        text = Text(content=content)
        db.session.add(text)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        texts = Text.query.all()
        return render_template('index.html', texts=texts, files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    
    if file:
        file.save(os.path.join(
            app.config['UPLOAD_DIRECTORY'],
            secure_filename(file.filename)
        ))
    
    return redirect('/')

@app.route('/serve-files/<filename>', methods=['GET'])
def serve_files(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)

if  __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    





