import os

APP_PATH = os.path.dirname(__file__)
TEMPLATES_PATH = os.path.join(APP_PATH, 'templates')
STATIC_PATH = os.path.join(APP_PATH, 'static')
UPLOAD_FOLDER = os.path.join(STATIC_PATH, 'uploaded')
RESULT_FOLDER = os.path.join(STATIC_PATH, 'result')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}