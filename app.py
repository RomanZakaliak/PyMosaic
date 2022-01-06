"""
This file isn't anymore  part of PyMosaic and it leaved here only 
to ensure that all features ported to new aiohttp version

You may ignore it or even delete
All errors which you may aquire does not effect on 
working of aiohttp part of application
and could be ignored
"""

import os
import secrets
import logging

import asyncio


from src.image import Pixelize


log = logging.getLogger(__name__)


APP_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(APP_PATH, 'static')
UPLOAD_FOLDER = os.path.join(STATIC_PATH, 'uploaded')
RESULT_FOLDER = os.path.join(STATIC_PATH, 'result')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
if not os.path.exists(RESULT_FOLDER):
    os.mkdir(RESULT_FOLDER)

routes = web.RouteTableDef()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = secrets.token_hex(30)

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    return '.' in filename and \
            get_file_extension(filename) in ALLOWED_EXTENSIONS

def process_file(filename, coords, chunk_size):
    pixelize = Pixelize(os.path.join(UPLOAD_FOLDER, filename))
    pixelize.divide_onto_chunks(coords, chunk_size)
    pixelize.save_new_file(destination=RESULT_FOLDER, output_file_name=filename)


@routes.get('/')
async def index(file_name:str = None):
    return render_template('index.html.jinja')

def correct_coords(coords: dict)->dict:
    if coords['x1'] > coords['x2']:
        coords['x1'], coords['x2'] = coords['x2'], coords['x1']

    if coords['y1'] > coords['y2']:
        coords['y1'], coords['y2'] = coords['y2'], coords['y1']

    return coords

@app.route('/upload_file', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        req_files = request.files
        req_form = request.form
        if 'file' not in req_files or 'chunk_size' not in req_form:
            return redirect(request.url)

        file = req_files['file']
        chunk_size = int(req_form['chunk_size'])
        keys = ['x1', 'y1', 'x2', 'y2']
        coords = dict()
        for key in keys:
            coords[key] = int(float(req_form[key]))
        coords = correct_coords(coords)

        if file.filename == '':
            return redirect(request.url)

        file_extension = get_file_extension(file.filename)
        file.filename = f'{secrets.token_hex(10)}.{file_extension}'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_filename)
            process_file(filename, coords, chunk_size)
            res = jsonify({'filename':str(filename)})
            return make_response(res)

@app.route('/download/<string:filename>')
def download_file(filename):
    accessed_filename = os.path.join(RESULT_FOLDER, filename)
    if os.path.isfile(accessed_filename):
        return send_from_directory(directory=RESULT_FOLDER, filename=filename)
    else:
        raise Exception("File does not exists")

@app.errorhandler(Exception)
def handle_exception(exp):
    return render_template('error.html.jinja', error=exp)

if __name__ == "__main__": app.run(debug=True, host='0.0.0.0')