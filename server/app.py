import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import subprocess

# set up text to speech map
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# speech recognition
import speech_recognition as sr
recognizer = sr.Recognizer()

# Create dictionary
word_dict = dict()
stem_dict = dict()

# Create stemmer
stemmer = PorterStemmer()

# Read in the dictionary file
dict_dir = "../img/"
dict_filename = dict_dir + "dict.txt"
dict_file = open(dict_filename, "r")
dict_lines = dict_file.read().splitlines()

# Make map of word and word stem to file
for line in dict_lines:
	split = line.split()
	word = split[0]
	filepath = dict_dir + split[1]
	if word not in word_dict.keys():
		word_dict[word] = "https://raw.githubusercontent.com/LeartKrasniqi/Sign-Language-Translator/post-covid-19/img/words/" + word + ".png"

	stem = stemmer.stem(word)
	if stem not in stem_dict.keys():
		stem_dict[stem] = "https://raw.githubusercontent.com/LeartKrasniqi/Sign-Language-Translator/post-covid-19/img/words/" + word + ".png"

# Translate the sentences
#    takes recognized_words as input and
#    returns a valid path to each word or letter
def text2imgpath(recognized_words):
    # sample file that contains a few lines of text:
    # sentences_file = open("../text2img/tests/sentences.txt", "r")
    words = recognized_words
    img_links = []
    for s in words:
        tokens = word_tokenize(s)
        for t in tokens:
            t = t.lower()
            wordstem = stemmer.stem(t)
            if t in word_dict.keys():
                # word image
                img_links.append(word_dict[t])
            elif wordstem in stem_dict.keys():
                img_links.append(stem_dict[wordstem])
            else:
                # letter image
                chars = list(t)
                for c in chars:
                    path = "https://raw.githubusercontent.com/LeartKrasniqi/Sign-Language-Translator/post-covid-19/img/letters/{}.png".format(c)
                    img_links.append(path)
    return img_links
# set up server
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
        audiopath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audionewpath = os.path.join(app.config['UPLOAD_FOLDER'], "myaudio.wav")
        file.save(audiopath)

        command = "ffmpeg -i " + audiopath + " -ab 160k -ac 2 -y -ar 44100 -vn " + audionewpath
        os.system(command)
        speech = sr.AudioFile(audionewpath)
        with speech as audio_file:
            try:
                recognizer.adjust_for_ambient_noise(audio_file)
                audio = recognizer.record(audio_file, offset = 0)
                # list of recognized words in list
                recog_words = recognizer.recognize_google(audio).lower().split(",!? ")
                # get image path for the word
                imgpath = text2imgpath(recog_words)
                return(jsonify(imgpath))
                    #
                    # TODO: display to the front end HERE
                    #
            except Exception as e:
                print("Exception found!: {}: {}".format(type(e), e.message))

    return "success"

@app.route('/audiovideo', methods=['POST','GET'])
def audiovideo():
    if request.method == 'POST':
        file = request.files['audiovideo']
        filename = "myaudiovideo.webm"
        filename = secure_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify(status="success", text="blah")

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
