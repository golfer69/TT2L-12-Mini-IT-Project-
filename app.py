from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os 

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_DIRECTORY'])
    return render_template('index.html', files=files)

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
    app.run(debug=True)





