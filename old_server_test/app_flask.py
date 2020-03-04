from flask import Flask, jsonify
import werkzeug as wz
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/translate/ASL', methods=['GET', 'POST'])
def convert_ASL_to_text():
    imagefile = flask.request.files['image']
    filename = wz.utils.secure_filename(imagefile.filename)
    imagefile.save(filename)
    test_return = {
        'text': imagefile.filename,
        'number': 20,
        'boolean': True
    }
    return jsonify(test_return)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
