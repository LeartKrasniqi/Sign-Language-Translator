import os
from flask import Flask, flash, request, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './videos/'
ALLOWED_EXTENSIONS = {'mpg', 'mp4'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/audio',methods=['POST', 'GET'])
def audio():
    if request.method == 'POST':
        file = request.files['audio']
        filename = "myaudio.webm"
        filename = secure_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "success"

@app.route('/video',methods=['POST','GET'])
def video():
    if request.method == 'POST':
        file = request.files['video']
        filename = "myvideo.webm"
        filename = secure_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "success"

@app.route('/audiovideo', methods=['POST','GET'])
def audiovideo():
    if request.method == 'POST':
        file = request.files['audiovideo']
        filename = "myaudiovideo.webm"
        filename = secure_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "success"

@app.route('/api/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
        '''


if __name__ == '__main__':
    app.run(host="localhost", port=42248, debug=True)