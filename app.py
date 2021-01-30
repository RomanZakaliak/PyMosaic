import os
import secrets
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from src.image import ImageTransform


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploaded/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__, static_url_path = '', static_folder = './static/', template_folder = './templates/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = secrets.token_hex(30)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET'])
def index(file_name:str = None):
    return render_template('index.html.jinja')

@app.route('/upload_file', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))

if __name__ == "__main__": app.run(debug=True)